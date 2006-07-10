"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application. It's generally
assumed that it will be called by Paste, though any WSGI application server could create
and call the WSGI app as well.

"""
import sys
import re

import paste.wsgiwrappers
from paste.registry import RegistryManager
from paste.wsgiwrappers import WSGIRequest
from paste.wsgiwrappers import WSGIResponse

from routes import request_config
import myghty.escapes as escapes

import pylons
import pylons.templating
from pylons.util import RequestLocal
from pylons.helpers import Myghty_Compat, redirect_to

class PylonsBaseWSGIApp(object):
    """Basic Pylons WSGI Application

    This basic WSGI app is provided should a web developer want to
    get access to the most basic Pylons web application environment
    available. By itself, this Pylons web application does little more
    than dispatch to a controller and setup the context object, the
    request object, and the globals object.
    
    Additional functionality like sessions, and caching can be setup by
    altering the ``environ['pylons.environ_config']`` setting to indicate
    what key the ``session`` and ``cache`` functionality should come from.
    
    Resolving the URL and dispatching can be customized by sub-classing or
    "monkey-patching" this class. Subclassing is the preferred approach.
    
    """
    def __init__(self, mapper, package_name, globals, default_charset='UTF-8'):
        self.mapper = mapper
        self.globals = globals
        self.package_name = package_name
        self.default_charset = default_charset
        self.settings = dict(charset=default_charset, content_type='text/html')
        self.c = RequestLocal()
        config = globals.pylons_config
        
        # Initialize Buffet and all our template engines, default engine is the
        # first in the template_engines list
        def_eng = config.template_engines.pop(0)
        self.buffet = pylons.templating.Buffet(def_eng['engine'], 
            template_root=def_eng['template_root'], **def_eng['template_options'])
        for e in config.template_engines:
            self.buffet.prepare(e['engine'], template_root=e['template_root'], 
                alias=e['alias'], **e['template_options'])
    
    def __call__(self, environ, start_response):
        self.setup_app_env(environ, start_response)
        if environ.get('paste.testing'):
            self.load_test_env(environ)
        
        # Change our HTTP_METHOD if _method is present
        req = pylons.request.current_obj()
        old_method = None
        if req.params.has_key('_method'):
            old_method = environ['REQUEST_METHOD']
            environ['REQUEST_METHOD'] = req.params['_method']
        
        controller = self.resolve(environ, start_response)
        if old_method: environ['REQUEST_METHOD'] = old_method            
        response = self.dispatch(controller, environ, start_response)
        
        if environ.get('paste.testing') and hasattr(response, 'wsgi_response'):
            environ['paste.testing_variables']['response'] = response
        
        # Transform HttpResponse objects into WSGI response
        if hasattr(response, 'wsgi_response'):
            status, response_headers, content = response.wsgi_response()
            start_response(status, response_headers)
            return content
        elif response:
            return response
        else:
            # Apparently we returned absolutely nothing, use the response
            # object if in legacy mode, otherwise raise an exception
            if environ.get('pylons.legacy'):
                resp = pylons.helpers.response
                if hasattr(pylons.helpers.response, 'wsgicall'):
                    # Legacy app using run_wsgi
                    return resp.content
                status, response_headers, content = resp.wsgi_response()
                start_response(status, response_headers)
                return content
            else:
                raise Exception, "No content returned by controller: %s" % controller.__name__
    
    def setup_app_env(self, environ, start_response):
        """Setup and register all the Pylons objects with the registry"""
        req = WSGIRequest(environ)
        environ['paste.registry'].register(paste.wsgiwrappers.settings, self.settings)
        environ['paste.registry'].register(pylons.request, req)
        environ['paste.registry'].register(pylons.c, self.c)
        environ['paste.registry'].register(pylons.g, self.globals)
        environ['paste.registry'].register(pylons.params, req.params)
        environ['paste.registry'].register(pylons.buffet, self.buffet)
        pylons.h()
        self.c._clear()
        
        # Setup legacy globals
        if environ.get('pylons.legacy'):
            environ['paste.registry'].register(pylons.helpers.response, WSGIResponse())
            environ['paste.registry'].register(pylons.m, Myghty_Compat(environ, start_response))
        
        econf = environ['pylons.environ_config']
        if econf.get('session'):
            environ['paste.registry'].register(pylons.session, environ[econf['session']])
        if econf.get('cache'):
            environ['paste.registry'].register(pylons.cache, environ[econf['cache']])
    
    def resolve(self, environ, start_response):
        """Implements Routes-based dispatching"""
        config = request_config()
        config.mapper = self.mapper
        config.environ = environ
        config.redirect = redirect_to
        match = config.mapper_dict
        if not match:
            return None
        environ['pylons.routes_dict'] = match
        controller = match.get('controller')
        if not controller:
            return None
        
        # Pull the controllers class name, import controller
        # @@ TODO: Encapsulate in try/except to raise error if controller
        #          doesn't exist, or class in controller file doesn't exist.
        controller_name = self.package_name + '.controllers.' \
            + controller.lower().replace('/', '.')
        __import__(controller_name)
        controller_class = controller.split('/')[-1].title().replace('-', '_')
        classname = controller_class + 'Controller'
        controller = getattr(sys.modules[controller_name], classname)
        return controller
        
    def dispatch(self, controller, environ, start_response):
        """Dispatches to a controller, will instantiate the controller
        if necessary"""
        if not controller:
            res = WSGIResponse()
            res.status_code = 404
            return res
        match = environ['pylons.routes_dict']
        if not getattr(controller, 'wsgi_application', False):
            # Sanitaze keys
            # @@ TODO: This should be done in a lazy fashion
            for k,v in match.iteritems():
                if v:
                    match[k] = escapes.url_unescape(v)
            controller = controller()
            controller.start_response = start_response
            
            # @@ LEGACY: Attach c to controller
            if environ.get('pylons.legacy'):
                controller.c = pylons.c
            
            return controller(**match)
        
        self.fixup_environ(environ, match)
        return controller.wsgi_application(environ, start_response)
    
    def fixup_environ(self, environ, dispatch):
        """Fixes the environ based on the Routes match"""
        oldpath = environ['PATH_INFO']
        newpath = dispatch.get('path_info') or ''
        environ['PATH_INFO'] = newpath
        if not environ['PATH_INFO'].startswith('/'):
            environ['PATH_INFO'] = '/' + environ['PATH_INFO']
        environ['SCRIPT_NAME'] += re.sub(r'^(.*?)/' + newpath + '$', r'\1', oldpath)
        if environ['SCRIPT_NAME'].endswith('/'):
            environ['SCRIPT_NAME'] = environ['SCRIPT_NAME'][:-1]
    
    def load_test_env(self, environ):
        """Sets up our Paste testing environment"""
        testenv = environ['paste.testing_variables']
        testenv['req'] = pylons.request.current_obj()
        testenv['c'] = pylons.c.current_obj()
        testenv['g'] = pylons.g.current_obj()
        econf = environ['pylons.environ_config']
        if econf.get('session'):
            testenv['session'] = environ[econf['session']]
        if econf.get('cache'):
            testenv['cache'] = environ[econf['cache']]
        
    
class PylonsApp(object):
    """Setup the Pylons default environment
    
    Pylons App sets up the basic Pylons app, and initializes the global
    object, sessions and caching. Sessions and caching can be overridden
    in the config object by supplying other keys to look for in the environ
    where objects for the session/cache will be. If they're set to none,
    then no session/cache objects will be available.
    
    """
    def __init__(self, config, default_charset='UTF-8'):
        self.config = config
        g = None
        try:
            package = __import__(config.package + '.lib.app_globals', globals(), locals(), ['Globals'])
        except ImportError:
            pass
        else:
            g = package.Globals(config.global_conf, config.app_conf, config=config)
            g.pylons_config = config
        
        # Create the base Pylons wsgi app
        app = PylonsBaseWSGIApp(config.map, config.package, g, default_charset)
        
        # Pull user-specified environ overrides, or just setup default
        # session and caching objects
        self.econf = econf = config.environ_config.copy()
        if not econf.has_key('session'):
            from beaker.session import SessionMiddleware
            econf['session'] = 'beaker.session'
            app = SessionMiddleware(app, config.global_conf, 
                auto_register=True, **config.app_conf)
        
        if not econf.has_key('cache'):
            from beaker.cache import CacheMiddleware
            econf['cache'] = 'beaker.cache'
            app = CacheMiddleware(app, config.global_conf, **config.app_conf)
        
        self.globals = g
        self.app = app
    
    def __call__(self, environ, start_response):
        environ['pylons.environ_config'] = self.econf
        return self.app(environ, start_response)

class LegacyApp(object):
    def __init__(self, config):
        self.app = PylonsApp(config)
        self.globals = self.app.globals
    
    def __call__(self, environ, start_response):
        environ['pylons.legacy'] = True
        return self.app(environ, start_response)

def make_app(config):
    """ Legacy WSGI app creator"""
    papp = LegacyApp(config)
    from paste.deploy.config import ConfigMiddleware
    app = ConfigMiddleware(papp, {
        'default':config.global_conf,
        'app':config.app_conf,
        'app_conf':config.app_conf,
        'global_conf':config.global_conf
    })
    app = RegistryManager(app)
    app.globals = papp.globals
    return app

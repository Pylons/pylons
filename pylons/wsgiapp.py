"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application. It's generally
assumed that it will be called by Paste, though any WSGI application server could create
and call the WSGI app as well.

"""
import sys
import re
import inspect
import urllib
import warnings

import paste.wsgiwrappers
import paste.httpexceptions as httpexceptions
from paste.registry import RegistryManager
from paste.wsgiwrappers import WSGIRequest

from routes import request_config

import pylons
import pylons.templating
import pylons.legacy
from pylons.util import ContextObj, AttribSafeContextObj, _Translator, class_name_from_module_name
from pylons.controllers import Controller, WSGIController

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
    def __init__(self, mapper, package_name, globals, default_charset=None):
        self.mapper = mapper
        self.globals = globals
        self.package_name = package_name
        config = globals.pylons_config
        if default_charset:
            warnings.warn(
                "The 'default_charset' keyword argument to the PylonsBaseWSGIApp "
                "constructor is deprecated. Please specify 'default_charset' to the Config "
                'object in your config/environment.py file instead, e.g.:\n'
                'return pylons.config.Config(myghty, map, paths, '
                "default_charset='%s')" % default_charset, DeprecationWarning, 2)
            config.default_charset = default_charset
        self.settings = dict(content_type='text/html', charset=config.default_charset)
        
        # Create the redirect function we'll use and save it
        def redirect_to(url):
            raise httpexceptions.HTTPFound(url)
        self.redirect_to = redirect_to
        
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
        
        # Change our HTTP_METHOD if _method is present, try GET first to avoid
        # parsing POST unless absolutely necessary.
        req = pylons.request._current_obj()
        old_method = None
        if '_method' in environ['QUERY_STRING'] and req.GET.has_key('_method'):
            old_method = environ['REQUEST_METHOD']
            environ['REQUEST_METHOD'] = req.GET['_method']
        elif environ['REQUEST_METHOD'] == 'POST' and req.POST.has_key('_method'):
            old_method = environ['REQUEST_METHOD']
            environ['REQUEST_METHOD'] = req.POST['_method']
        
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
            
        # Apparently we returned absolutely nothing, use the response
        # object if in legacy mode, otherwise raise an exception
        if environ.get('pylons.legacy'):
            resp = pylons.legacy.response
            if hasattr(pylons.legacy.response, 'wsgicall'):
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
        
        # This is a legacy test for pre-0.9.2 projects to continue using the old
        # style Helper. New style directly uses the projects lib.helpers module
        # for 'normal' Python import usage with no surprises.
        __import__(self.package_name + '.lib.base')
        their_h = getattr(sys.modules[self.package_name + '.lib.base'], 'h', None)

        try: 
            helpers_name = self.package_name + '.config.helpers' 
            __import__(helpers_name) 
        except: 
            helpers_name = self.package_name + '.lib.helpers' 
            __import__(helpers_name)
        if their_h != pylons.h and their_h is not None:
            # We're using the new Helper import style
            req._h = sys.modules[helpers_name]
        else:
            # We still need to keep a reference to their helpers for the old
            # Helpers object.
            req._oldh = sys.modules[helpers_name]
        
        # Setup the translator global object
        trans = dict(translator=_Translator())
        trans['CONFIG'] = dict(app_conf=self.globals.pylons_config.app_conf,
            global_conf=self.globals.pylons_config.global_conf)
        if self.globals.pylons_config.app_conf.has_key('lang'):
            trans['translator'](self.globals.pylons_config.app_conf['lang'])
        else:
            trans['lang'] = None
        environ['paste.registry'].register(pylons.translator, trans)
        
        # Setup the basic pylons global objects
        environ['paste.registry'].register(paste.wsgiwrappers.settings, self.settings)
        environ['paste.registry'].register(pylons.request, req)
        if self.globals.pylons_config.strict_c:
            environ['paste.registry'].register(pylons.c, ContextObj())
        else:
            environ['paste.registry'].register(pylons.c, AttribSafeContextObj())
        environ['paste.registry'].register(pylons.g, self.globals)
        environ['paste.registry'].register(pylons.buffet, self.buffet)
        
        # Setup legacy globals
        if environ.get('pylons.legacy'):
            # Legacy mixed dictionary instead of MultiDict
            req._legacy_params = req.params.mixed()
            environ['paste.registry'].register(pylons.legacy.response, WSGIResponse())
            environ['paste.registry'].register(pylons.m, 
                pylons.legacy.Myghty_Compat(environ, start_response))
            environ['paste.registry'].register(pylons.params, req._legacy_params)
        
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
        config.redirect = self.redirect_to
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
        full_module_name = self.package_name + '.controllers.' \
            + controller.replace('/', '.')
        
        __import__(full_module_name)
        module_name = controller.split('/')[-1]
        class_name = class_name_from_module_name(module_name) + 'Controller'
        return getattr(sys.modules[full_module_name], class_name)
        
    def dispatch(self, controller, environ, start_response):
        """Dispatches to a controller, will instantiate the controller if
        necessary"""
        if not controller:
            raise httpexceptions.HTTPNotFound()
        match = environ['pylons.routes_dict']
        
        # Sanitize keys
        # @@ TODO: This should be done in a lazy fashion
        for k,v in match.iteritems():
            if v:
                match[k] = urllib.unquote_plus(v)
        
        # Older subclass of Controller
        if inspect.isclass(controller) and not issubclass(controller, WSGIController) and \
                issubclass(controller, Controller):
            controller = controller()
            controller.start_response = start_response
            
            # @@ LEGACY: Attach c to controller
            if environ.get('pylons.legacy'):
                controller.c = pylons.c
            
            return controller(**match)
        
        # If the route included a path_info attribute, we'll assume it
        # should be pulled, otherwise we call the controller    
        if match.get('path_info'):
            self.fixup_environ(environ, match)
        
        # If it's a class, instantiate it
        if not hasattr(controller, '__class__') or \
            getattr(controller, '__class__') == type:
            controller = controller()
        
        # Controller is assumed to handle a WSGI call
        return controller(environ, start_response)
    
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
        testenv['req'] = pylons.request._current_obj()
        testenv['c'] = pylons.c._current_obj()
        testenv['g'] = pylons.g._current_obj()
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
    def __init__(self, config, default_charset=None):
        self.config = config
        if default_charset:
            warnings.warn(
                "The 'default_charset' keyword argument to the PylonsApp constructor is "
                "deprecated. Please specify 'default_charset' to the Config object in your "
                'config/environment.py file instead, e.g.:\n'
                'return pylons.config.Config(myghty, map, paths, '
                "default_charset='%s')" % default_charset, DeprecationWarning, 2)
            self.config.default_charset = default_charset

        g = None
        try:
            package = __import__(config.package + '.lib.app_globals', globals(), locals(), ['Globals'])
        except ImportError:
            pass
        else:
            g = package.Globals(config.global_conf, config.app_conf, config=config)
            g.pylons_config = config
        
        # Create the base Pylons wsgi app
        app = PylonsBaseWSGIApp(config.map, config.package, g)
        
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

WSGIResponse = None

class LegacyApp(object):
    def __init__(self, config):
        global WSGIResponse
        from paste.wsgiwrappers import WSGIResponse
        self.app = PylonsApp(config)
        self.globals = self.app.globals
    
    def __call__(self, environ, start_response):
        environ['pylons.legacy'] = True
        return self.app(environ, start_response)

def make_app(config):
    """ Legacy WSGI app creator"""
    warnings.warn(
        "Legacy WSGI app in use for pre-0.9 application. This will be "
        "removed at some point post-1.0 which will require minor updates "
        "to your application.",
        DeprecationWarning, 2)
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

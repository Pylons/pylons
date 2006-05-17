"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application. It's generally
assumed that it will be called by Paste, though any WSGI application server could create
and call the WSGI app as well.

"""
import sys

import paste.wsgiwrappers
from paste.wsgiwrappers import WSGIRequest, WSGIResponse

from routes import request_config
import myghty.escapes as escapes

import pylons

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
    
    def __call__(self, environ, start_response):
        self.setup_app_env(environ)
        if environ.get('paste.testing'):
            self.load_test_env(environ)
        
        controller = self.resolve(environ, start_response)
        response = self.dispatch(controller, environ, start_response)
        
        # Transform HttpResponse objects into WSGI response
        if hasattr(response, 'wsgi_response'):
            status, response_headers, content = response.wsgi_response()
            start_response(status, response_headers)
            return content
        else:
            return response
    
    def setup_app_env(self, environ):
        """Setup and register all the Pylons objects with the registry"""
        req = WSGIRequest(environ)
        environ['paste.registry'].register(paste.wsgiwrappers.settings, self.settings)
        environ['paste.registry'].register(pylons.request, req)
        environ['paste.registry'].register(pylons.c, {})
        environ['paste.registry'].register(pylons.g, self.globals)
        environ['paste.registry'].register(pylons.params, req.params)
        environ['paste.registry'].register(pylons.response, WSGIResponse())
        pylons.h()
        
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
        match = config.mapper_dict
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
            pylons.response.status_code = 404
            return pylons.response
        match = environ['pylons.routes_dict']
        if not getattr(controller, 'wsgi_application', False):
            # Sanitaze keys
            # @@ TODO: This should be done in a lazy fashion
            for k,v in match.iteritems():
                if v:
                    match[k] = escapes.url_unescape(v)
            controller = controller()
            controller.start_response = start_response
            return controller(**match)
        
        self.fixup_environ(environ, match)
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
        testenv['request'] = pylons.request.current_obj()
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
    def __init__(self, config):
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
        app = PylonsBaseWSGIApp(config.map, config.package, g)
        
        # Pull user-specified environ overrides, or just setup default
        # session and caching objects
        self.econf = econf = config.environ_config.copy()
        if not econf.has_key('session'):
            from beaker.session import SessionMiddleware
            econf['session'] = 'beaker.session'
            app = SessionMiddleware(app, config.global_conf, **config.app_conf)
        
        if not econf.has_key('cache'):
            from beaker.cache import CacheMiddleware
            econf['cache'] = 'beaker.cache'
            app = CacheMiddleware(app, config.global_conf, **config.app_conf)
        
        self.globals = g
        self.app = app
    
    def __call__(self, environ, start_response):
        environ['pylons.environ_config'] = self.econf
        return self.app(environ, start_response)

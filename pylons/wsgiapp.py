"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application.
It's generally assumed that it will be called by Paste, though any WSGI 
application server could create and call the WSGI app as well.
"""
import gettext
import sys
import inspect
import warnings

import paste.wsgiwrappers
import paste.httpexceptions as httpexceptions
import paste.registry
from paste.wsgiwrappers import WSGIRequest

from routes import request_config
from routes.middleware import RoutesMiddleware

import pylons
import pylons.legacy
import pylons.templating
from pylons.i18n import set_lang
from pylons.util import ContextObj, AttribSafeContextObj, class_name_from_module_name
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
    def __init__(self, package_name, globals, helpers=None):
        """Initialize a base Pylons WSGI application
        
        The base Pylons WSGI application requires several keywords, the package
        name, and the globals object. If no helpers object is provided then h
        will be None.
        """
        self.helpers = helpers
        self.globals = globals
        self.package_name = package_name
        config = globals.pylons_config
        self.settings = dict(content_type='text/html', 
                             charset=config.default_charset)
        
        # Create the redirect function we'll use and save it
        def redirect_to(url):
            raise httpexceptions.HTTPFound(url)
        self.redirect_to = redirect_to
        
        # Initialize Buffet and all our template engines, default engine is the
        # first in the template_engines list
        def_eng = config.template_engines[0]
        self.buffet = pylons.templating.Buffet(def_eng['engine'], 
            template_root=def_eng['template_root'], **def_eng['template_options'])
        for e in config.template_engines[1:]:
            self.buffet.prepare(e['engine'], template_root=e['template_root'], 
                alias=e['alias'], **e['template_options'])
    
    def __call__(self, environ, start_response):
        req = self.setup_app_env(environ, start_response)
        if 'paste.testing_variables' in environ:
            self.load_test_env(environ)
            if environ['PATH_INFO'] == '/_test_vars':
                paste.registry.restorer.save_registry_state(environ)
                start_response('200 OK', [('Content-type','text/plain')])
                return ['%s' % paste.registry.restorer.get_request_id(environ)]
        
        controller = self.resolve(environ, start_response)
        response = self.dispatch(controller, environ, start_response)
        
        if 'paste.testing_variables' in environ and hasattr(response, 'wsgi_response'):
            environ['paste.testing_variables']['response'] = response
        
        # Transform HttpResponse objects into WSGI response
        if hasattr(response, 'wsgi_response'):
            return response(environ, start_response)
        elif response:
            return response
        
        raise Exception, "No content returned by controller: %s" % controller.__name__
    
    def setup_app_env(self, environ, start_response):
        """Setup and register all the Pylons objects with the registry"""
        req = WSGIRequest(environ)
        
        registry = environ['paste.registry']
                
        # Setup the basic pylons global objects
        registry.register(paste.wsgiwrappers.settings, self.settings)
        registry.register(pylons.request, req)
        registry.register(pylons.buffet, self.buffet)
        registry.register(pylons.g, self.globals)
        registry.register(pylons.h, self.helpers or \
                          pylons.legacy.load_h(self.package_name))
        
        # Setup the translator global object
        registry.register(pylons.translator, gettext.NullTranslations())
        lang = self.globals.pylons_config.app_conf.get('lang')
        if lang:
            set_lang(lang)
        
        if self.globals.pylons_config.strict_c:
            registry.register(pylons.c, ContextObj())
        else:
            registry.register(pylons.c, AttribSafeContextObj())
        
        econf = environ['pylons.environ_config']
        if econf.get('session'):
            registry.register(pylons.session, environ[econf['session']])
        if econf.get('cache'):
            registry.register(pylons.cache, environ[econf['cache']])
        return req
    
    def resolve(self, environ, start_response):
        """Uses dispatching information found in 
        ``environ['wsgiorg.routing_args']`` to retrieve a controller name and
        return the controller instance from the appropriate controller 
        module"""
        # Update the Routes config object in case we're using Routes
        config = request_config()
        config.redirect = self.redirect_to
        match = environ['wsgiorg.routing_args'][1]
        
        environ['pylons.routes_dict'] = match
        controller = match.get('controller')
        if not controller:
            return None
        
        # Pull the controllers class name, import controller
        full_module_name = self.package_name + '.controllers.' \
            + controller.replace('/', '.')
        
        # Hide the traceback here if the import fails (bad syntax and such)
        __traceback_hide__ = 'before_and_this'
        
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
        
        # Older subclass of Controller
        if inspect.isclass(controller) and not issubclass(controller, WSGIController) and \
                issubclass(controller, Controller):
            controller = controller()
            controller.start_response = start_response
            
            return controller(**match)
                
        # If it's a class, instantiate it
        if not hasattr(controller, '__class__') or \
            getattr(controller, '__class__') == type:
            controller = controller()
        
        # Controller is assumed to handle a WSGI call
        return controller(environ, start_response)
    
    def load_test_env(self, environ):
        """Sets up our Paste testing environment"""
        testenv = environ['paste.testing_variables']
        testenv['req'] = pylons.request._current_obj()
        testenv['c'] = pylons.c._current_obj()
        testenv['g'] = pylons.g._current_obj()
        testenv['h'] = pylons.h._current_obj()
        testenv['pylons_config'] = self.globals.pylons_config
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
    def __init__(self, config, default_charset=None, helpers=None, g=None,
                 use_routes=True):
        self.config = config
        if default_charset:
            warnings.warn(
                "The 'default_charset' keyword argument to the PylonsApp constructor is "
                "deprecated. Please specify 'default_charset' to the Config object in your "
                'config/environment.py file instead, e.g.:\n'
                'return pylons.config.Config(myghty, map, paths, '
                "default_charset='%s')" % default_charset, DeprecationWarning, 2)
            self.config.default_charset = default_charset

        if helpers is None or g is None:
            warnings.warn(
                'Pylons 0.9.3 and above now explicitly pass helpers and g '
                'references to the PylonsApp constructor. Please update your '
                'middleware.py with:\n\n'
                '    import MYPROJ.lib.app_globals as app_globals\n'
                '    import MYPROJ.lib.helpers\n\n'
                'Then edit the PylonsApp instantiation with:\n\n'
                '    app = pylons.wsgiapp.PylonsApp(config, '
                'helpers=MYPROJ.lib.helpers,\n'
                '                                   g=app_globals.Globals)\n\n'
                'where MYPROJ is the name of your project.\n',
                DeprecationWarning, 2)
            
        if not g:
            try:
                globals_package = __import__(config.package + '.lib.app_globals',
                                             globals(), locals(), ['Globals'])
                g = getattr(globals_package, 'Globals')
            except ImportError:
                pass
        # Assign a default globals object, and instantiate it
        if not g:
            g = type("Globals", (), {})()
        else:
            g = g(config.global_conf, config.app_conf, config=config)
        g.pylons_config = config
        
        # Create the base Pylons wsgi app
        app = PylonsBaseWSGIApp(config.package, g, helpers=helpers)
        if use_routes:
            app = RoutesMiddleware(app, config.map)
        
        # Pull user-specified environ overrides, or just setup default
        # session and caching objects
        self.econf = econf = config.environ_config.copy()
        if 'session' not in econf:
            from beaker.session import SessionMiddleware
            econf['session'] = 'beaker.session'
            app = SessionMiddleware(app, config.global_conf, 
                auto_register=True, **config.app_conf)
        
        if 'cache' not in econf:
            from beaker.cache import CacheMiddleware
            econf['cache'] = 'beaker.cache'
            app = CacheMiddleware(app, config.global_conf, **config.app_conf)
        
        self.globals = g
        self.app = app
    
    def __call__(self, environ, start_response):
        environ['pylons.environ_config'] = self.econf
        return self.app(environ, start_response)

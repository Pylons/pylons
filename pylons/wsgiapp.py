"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application.
It's generally assumed that it will be called by Paste, though any WSGI 
application server could create and call the WSGI app as well.
"""
import gettext
import inspect
import logging
import sys
import warnings

import paste.httpexceptions as httpexceptions
import paste.registry
from paste.wsgiwrappers import WSGIRequest, WSGIResponse
from routes import request_config

import pylons
import pylons.legacy
import pylons.templating
from pylons.controllers import Controller, WSGIController
from pylons.i18n import set_lang
from pylons.util import ContextObj, AttribSafeContextObj, \
    class_name_from_module_name

__all__ = ['PylonsApp', 'PylonsBaseWSGIApp']

log = logging.getLogger(__name__)

class PylonsApp(object):
    """Pylons WSGI Application

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
    def __init__(self, **kwargs):
        """Initialize a base Pylons WSGI application
        
        The base Pylons WSGI application requires several keywords, the package
        name, and the globals object. If no helpers object is provided then h
        will be None.
        """
        self.config = config = pylons.config._current_obj()
        package_name = config['pylons.package']
        self.helpers = config['pylons.h']
        self.globals = config['pylons.g']
        self.package_name = package_name
        self.request_options = config['pylons.request_options']
        self.response_options = config['pylons.response_options']
        self.controller_classes = {}
        self.log_debug = False
        
        # Create the redirect function we'll use and save it
        def redirect_to(url):
            log.debug("Raising redirect to %s", url)
            raise httpexceptions.HTTPFound(url)
        self.redirect_to = redirect_to
        
        # Initialize Buffet and all our template engines, default engine is the
        # first in the template_engines list
        def_eng = config['buffet.template_engines'][0]
        self.buffet = pylons.templating.Buffet(
            def_eng['engine'], 
            template_root=def_eng['template_root'],
            **def_eng['template_options'])
        for e in config['buffet.template_engines'][1:]:
            log.debug("Initializing additional template engine: %s", e['engine'])
            self.buffet.prepare(e['engine'], template_root=e['template_root'], 
                alias=e['alias'], **e['template_options'])
    
    def __call__(self, environ, start_response):
        # Cache the logging level for the request
        log_debug = self.log_debug = logging.DEBUG >= log.getEffectiveLevel()

        self.setup_app_env(environ, start_response)
        if 'paste.testing_variables' in environ:
            self.load_test_env(environ)
            if environ['PATH_INFO'] == '/_test_vars':
                paste.registry.restorer.save_registry_state(environ)
                start_response('200 OK', [('Content-type', 'text/plain')])
                return ['%s' % paste.registry.restorer.get_request_id(environ)]
        
        controller = self.resolve(environ, start_response)
        response = self.dispatch(controller, environ, start_response)
        
        if 'paste.testing_variables' in environ and hasattr(response,
                                                            'wsgi_response'):
            environ['paste.testing_variables']['response'] = response
        
        if hasattr(response, 'wsgi_response'):
            # Transform Response objects from legacy Controller
            if log_debug:
                log.debug("Transforming legacy Response object into WSGI "
                          "response")
            return response(environ, start_response)
        elif response:
            return response
        
        raise Exception("No content returned by controller (Did you remember "
                        "to 'return' it?) in: %r" % controller.__name__)
    
    def setup_app_env(self, environ, start_response):
        """Setup and register all the Pylons objects with the registry"""
        if self.log_debug:
            log.debug("Setting up Pylons stacked object globals")
        registry = environ['paste.registry']

        registry.register(WSGIRequest.defaults, self.request_options)
        registry.register(WSGIResponse.defaults, self.response_options)

        req = WSGIRequest(environ)
                
        # Setup the basic pylons global objects
        registry.register(pylons.request, req)
        registry.register(pylons.response, WSGIResponse())
        registry.register(pylons.buffet, self.buffet)
        registry.register(pylons.g, self.globals)
        registry.register(pylons.config, self.config)
        registry.register(pylons.h, self.helpers or \
                          pylons.legacy.load_h(self.package_name))
        
        # Setup the translator global object
        registry.register(pylons.translator, gettext.NullTranslations())
        lang = self.config.get('lang')
        if lang:
            set_lang(lang)
        
        if self.config['pylons.strict_c']:
            registry.register(pylons.c, ContextObj())
        else:
            registry.register(pylons.c, AttribSafeContextObj())
        
        econf = self.config['pylons.environ_config']
        if econf.get('session'):
            registry.register(pylons.session, environ[econf['session']])
        elif 'beaker.session' in environ:
            registry.register(pylons.session, environ['beaker.session'])
        if econf.get('cache'):
            registry.register(pylons.cache, environ[econf['cache']])
        elif 'beaker.cache' in environ:
            registry.register(pylons.cache, environ['beaker.cache'])
    
    def resolve(self, environ, start_response):
        """Uses dispatching information found in 
        ``environ['wsgiorg.routing_args']`` to retrieve a controller name and
        return the controller instance from the appropriate controller 
        module.
        
        Override this to change how the controller name is found and returned.
        """
        # Update the Routes config object in case we're using Routes
        config = request_config()
        config.redirect = self.redirect_to
        match = environ['wsgiorg.routing_args'][1]
        
        environ['pylons.routes_dict'] = match
        controller = match.get('controller')
        if not controller:
            return

        if self.log_debug:
            log.debug("Resolved URL to controller: %r", controller)
        return self.find_controller(controller)
    
    def find_controller(self, controller):
        """Locates a controller by attempting to import it then grab the 
        SomeController instance from the imported module.
        
        Override this to change how the controller object is found once the URL
        has been resolved.
        """
        # Check to see if we've cached the class instance for this name
        if controller in self.controller_classes:
            return self.controller_classes[controller]
        
        # Pull the controllers class name, import controller
        full_module_name = self.package_name + '.controllers.' \
            + controller.replace('/', '.')
        
        # Hide the traceback here if the import fails (bad syntax and such)
        __traceback_hide__ = 'before_and_this'
        
        __import__(full_module_name)
        module_name = controller.split('/')[-1]
        class_name = class_name_from_module_name(module_name) + 'Controller'
        if self.log_debug:
            log.debug("Found controller, module: '%s', class: '%s'",
                      full_module_name, class_name)
        self.controller_classes[controller] = mycontroller = \
            getattr(sys.modules[full_module_name], class_name)
        return mycontroller
        
    def dispatch(self, controller, environ, start_response):
        """Dispatches to a controller, will instantiate the controller if
        necessary.
        
        Override this to change how the controller dispatch is handled.
        """
        log_debug = self.log_debug
        if not controller:
            if log_debug:
                log.debug("No controller found, returning 404 HTTP Not Found")
            not_found = httpexceptions.HTTPNotFound()
            return not_found.wsgi_application(environ, start_response)

        match = environ['pylons.routes_dict']
        
        # Older subclass of Controller
        if inspect.isclass(controller) and \
                not issubclass(controller, WSGIController) and \
                issubclass(controller, Controller):
            controller = controller()
            controller.start_response = start_response
            controller._pylons_log_debug = log_debug
            if log_debug:
                log.debug("Calling older Controller subclass")
            return controller(**match)
        
        # If it's a class, instantiate it
        if not hasattr(controller, '__class__') or \
            getattr(controller, '__class__') == type:
            if log_debug:
                log.debug("Controller appears to be a class, instantiating")
            controller = controller()
            controller._pylons_log_debug = log_debug
        
        # Controller is assumed to handle a WSGI call
        if log_debug:
            log.debug("Calling controller class with WSGI interface")
        return controller(environ, start_response)
    
    def load_test_env(self, environ):
        """Sets up our Paste testing environment"""
        if self.log_debug:
            log.debug("Setting up paste testing environment variables")
        testenv = environ['paste.testing_variables']
        testenv['req'] = pylons.request._current_obj()
        testenv['c'] = pylons.c._current_obj()
        testenv['g'] = pylons.g._current_obj()
        testenv['h'] = self.config['pylons.h'] or pylons.h._current_obj()
        testenv['config'] = self.config
        econf = self.config['pylons.environ_config']
        if econf.get('session'):
            testenv['session'] = environ[econf['session']]
        elif 'beaker.session' in environ:
            testenv['session'] = environ['beaker.session']
        if econf.get('cache'):
            testenv['cache'] = environ[econf['cache']]
        elif 'beaker.cache' in environ:
            testenv['cache'] = environ['beaker.cache']

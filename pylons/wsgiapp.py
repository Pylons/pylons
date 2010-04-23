"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI
application (PylonsApp). It's generally assumed that it will be called
by Paste, though any WSGI server could create and call the WSGI app as
well.

"""
import logging
import sys

import paste.registry
import pkg_resources
from webob.exc import HTTPFound, HTTPNotFound

import pylons
import pylons.templating
from pylons.controllers.util import Request, Response
from pylons.i18n.translation import _get_translator
from pylons.util import (AttribSafeContextObj, ContextObj, PylonsContext,
                         class_name_from_module_name)

__all__ = ['PylonsApp']

log = logging.getLogger(__name__)

class PylonsApp(object):
    """Pylons WSGI Application

    This basic WSGI app is provided should a web developer want to
    get access to the most basic Pylons web application environment
    available. By itself, this Pylons web application does little more
    than dispatch to a controller and setup the context object, the
    request object, and the globals object.
    
    Additional functionality like sessions, and caching can be setup by
    altering the ``environ['pylons.environ_config']`` setting to
    indicate what key the ``session`` and ``cache`` functionality
    should come from.
    
    Resolving the URL and dispatching can be customized by sub-classing
    or "monkey-patching" this class. Subclassing is the preferred
    approach.
    
    """
    def __init__(self, config=None, **kwargs):
        """Initialize a base Pylons WSGI application
        
        The base Pylons WSGI application requires several keywords, the
        package name, and the globals object. If no helpers object is
        provided then h will be None.
        
        """
        self.config = config = config or pylons.config._current_obj()
        package_name = config['pylons.package']
        self.helpers = config['pylons.h']
        self.globals = config.get('pylons.app_globals')
        self.environ_config = config['pylons.environ_config']
        self.package_name = package_name
        self.request_options = config['pylons.request_options']
        self.response_options = config['pylons.response_options']
        self.controller_classes = {}
        self.log_debug = False
        self.config.setdefault('lang', None)
        
        # Create the redirect function we'll use and save it
        def redirect_to(url):
            log.debug("Raising redirect to %s", url)
            raise HTTPFound(location=url)
        self.redirect_to = redirect_to
                
        # Cache some options for use during requests
        self._session_key = self.environ_config.get('session', 'beaker.session')
        self._cache_key = self.environ_config.get('cache', 'beaker.cache')
    
    def __call__(self, environ, start_response):
        """Setup and handle a web request
        
        PylonsApp splits its functionality into several methods to
        make it easier to subclass and customize core functionality.
        
        The methods are called in the following order:
        
        1. :meth:`~PylonsApp.setup_app_env`
        2. :meth:`~PylonsApp.load_test_env` (Only if operating in
           testing mode)
        3. :meth:`~PylonsApp.resolve`
        4. :meth:`~PylonsApp.dispatch`
        
        The response from :meth:`~PylonsApp.dispatch` is expected to be
        an iterable (valid :pep:`333` WSGI response), which is then
        sent back as the response.
        
        """
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
        
        try:
            if hasattr(response, 'wsgi_response'):
                # Transform Response objects from legacy Controller
                if log_debug:
                    log.debug("Transforming legacy Response object into WSGI "
                              "response")
                return response(environ, start_response)
            elif response is not None:
                return response
        
            raise Exception("No content returned by controller (Did you "
                            "remember to 'return' it?) in: %r" %
                            controller.__name__)
        finally:
            # Help Python collect ram a bit faster by removing the reference 
            # cycle that the pylons object causes
            if 'pylons.pylons' in environ:
                del environ['pylons.pylons']
    
    def register_globals(self, environ):
        """Registers globals in the environment, called from
        :meth:`~PylonsApp.setup_app_env`
        
        Override this to control how the Pylons API is setup. Note that
        a custom render function will need to be used if the 
        ``pylons.app_globals`` global is not available.
        
        """
        pylons_obj = environ['pylons.pylons']
        
        registry = environ['paste.registry']
        registry.register(pylons.response, pylons_obj.response)
        registry.register(pylons.request, pylons_obj.request)
        
        registry.register(pylons.app_globals, self.globals)
        registry.register(pylons.config, self.config)
        registry.register(pylons.tmpl_context, pylons_obj.tmpl_context)
        registry.register(pylons.translator, pylons_obj.translator)
        
        if 'session' in pylons_obj.__dict__:
            registry.register(pylons.session, pylons_obj.session)
        if 'cache' in pylons_obj.__dict__:
            registry.register(pylons.cache, pylons_obj.cache)
        elif 'cache' in pylons_obj.app_globals.__dict__:
            registry.register(pylons.cache, pylons_obj.app_globals.cache)
        
        if 'routes.url' in environ:
            registry.register(pylons.url, environ['routes.url'])
    
    def setup_app_env(self, environ, start_response):
        """Setup and register all the Pylons objects with the registry
        
        After creating all the global objects for use in the request,
        :meth:`~PylonsApp.register_globals` is called to register them
        in the environment.
        
        """
        if self.log_debug:
            log.debug("Setting up Pylons stacked object globals")
        
        
        # Setup the basic pylons global objects
        req_options = self.request_options
        req = Request(environ, charset=req_options['charset'],
                      unicode_errors=req_options['errors'],
                      decode_param_names=req_options['decode_param_names'])
        req.language = req_options['language']
        
        response = Response(
            content_type=self.response_options['content_type'],
            charset=self.response_options['charset'])
        response.headers.update(self.response_options['headers'])
        
        # Store a copy of the request/response in environ for faster access
        pylons_obj = PylonsContext()
        pylons_obj.config = self.config
        pylons_obj.request = req
        pylons_obj.response = response
        pylons_obj.app_globals = self.globals
        pylons_obj.h = self.helpers
        
        if 'routes.url' in environ:
            pylons_obj.url = environ['routes.url']
                
        environ['pylons.pylons'] = pylons_obj
        
        environ['pylons.environ_config'] = self.environ_config
        
        # Setup the translator object
        lang = self.config['lang']
        pylons_obj.translator = _get_translator(lang, pylons_config=self.config)
        
        if self.config['pylons.strict_tmpl_context']:
            tmpl_context = ContextObj()
        else:
            tmpl_context = AttribSafeContextObj()
        pylons_obj.tmpl_context = tmpl_context
        
        econf = self.config['pylons.environ_config']
        if self._session_key in environ:
            pylons_obj.session = environ[self._session_key]
        if self._cache_key in environ:
            pylons_obj.cache = environ[self._cache_key]
        
        # Load the globals with the registry if around
        if 'paste.registry' in environ:
            self.register_globals(environ)
    
    def resolve(self, environ, start_response):
        """Uses dispatching information found in 
        ``environ['wsgiorg.routing_args']`` to retrieve a controller
        name and return the controller instance from the appropriate
        controller module.
        
        Override this to change how the controller name is found and
        returned.
        
        """
        match = environ['wsgiorg.routing_args'][1]
        environ['pylons.routes_dict'] = match
        controller = match.get('controller')
        if not controller:
            return

        if self.log_debug:
            log.debug("Resolved URL to controller: %r", controller)
        return self.find_controller(controller)
    
    def find_controller(self, controller):
        """Locates a controller by attempting to import it then grab
        the SomeController instance from the imported module.
        
        Controller name is assumed to be a module in the controllers
        directory unless it contains a '.' or ':' which is then assumed
        to be a dotted path to the module and name of the controller
        object.
        
        Override this to change how the controller object is found once
        the URL has been resolved.
        
        """
        # Check to see if we've cached the class instance for this name
        if controller in self.controller_classes:
            return self.controller_classes[controller]
        
        # Check to see if its a dotted name
        if '.' in controller or ':' in controller:
            mycontroller = pkg_resources.EntryPoint.parse(
                'x=%s' % controller).load(False)
            self.controller_classes[controller] = mycontroller
            return mycontroller
        
        # Pull the controllers class name, import controller
        full_module_name = self.package_name + '.controllers.' \
            + controller.replace('/', '.')
        
        # Hide the traceback here if the import fails (bad syntax and such)
        __traceback_hide__ = 'before_and_this'
        
        __import__(full_module_name)
        if hasattr(sys.modules[full_module_name], '__controller__'):
            mycontroller = getattr(sys.modules[full_module_name],
                sys.modules[full_module_name].__controller__)
        else:
            module_name = controller.split('/')[-1]
            class_name = class_name_from_module_name(module_name) + 'Controller'
            if self.log_debug:
                log.debug("Found controller, module: '%s', class: '%s'",
                          full_module_name, class_name)
            mycontroller = getattr(sys.modules[full_module_name], class_name)
        self.controller_classes[controller] = mycontroller
        return mycontroller
        
    def dispatch(self, controller, environ, start_response):
        """Dispatches to a controller, will instantiate the controller
        if necessary.
        
        Override this to change how the controller dispatch is handled.
        
        """
        log_debug = self.log_debug
        if not controller:
            if log_debug:
                log.debug("No controller found, returning 404 HTTP Not Found")
            return HTTPNotFound()(environ, start_response)

        # If it's a class, instantiate it
        if hasattr(controller, '__bases__'):
            if log_debug:
                log.debug("Controller appears to be a class, instantiating")
            controller = controller()
            controller._pylons_log_debug = log_debug
        
        # Add a reference to the controller app located
        environ['pylons.controller'] = controller
        
        # Controller is assumed to handle a WSGI call
        if log_debug:
            log.debug("Calling controller class with WSGI interface")
        return controller(environ, start_response)
    
    def load_test_env(self, environ):
        """Sets up our Paste testing environment"""
        if self.log_debug:
            log.debug("Setting up paste testing environment variables")
        testenv = environ['paste.testing_variables']
        pylons_obj = environ['pylons.pylons']
        testenv['req'] = pylons_obj.request
        testenv['response'] = pylons_obj.response
        testenv['tmpl_context'] = pylons_obj.tmpl_context
        testenv['app_globals'] = testenv['g'] = pylons_obj.app_globals
        testenv['h'] = self.config['pylons.h']
        testenv['config'] = self.config
        if hasattr(pylons_obj, 'session'):
            testenv['session'] = pylons_obj.session
        if hasattr(pylons_obj, 'cache'):
            testenv['cache'] = pylons_obj.cache

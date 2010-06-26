"""The core WSGIController"""
import inspect
import logging
import types

from webob.exc import HTTPException, HTTPNotFound

import pylons
from pylons.events import NewResponse
from pylons.controllers.util import lookup_controller

__all__ = ['WSGIController']

log = logging.getLogger(__name__)


def map_responder(responder, package_name=None):
    """Given a responder name, handle looking it up and returning
    a callable responder"""
    # If its a string, determine if its a legacy controller name
    # or a resource specification
    if isinstance(responder, basestring):
        responder_result = lookup_controller(responder, package_name)
    else:
        responder_result = responder
    
    # If the controller is not a class, like we're expecting it
    # to be for a route handler, assume its a proper responder
    # and return it
    if not hasattr(responder_result, '__bases__'):
        if not callable(responder_result):
            raise Exception("Can't map %s to a valid callable responder, got"
                            " %r instead.", responder, responder_result)
        return responder_result
    
    # It must be a newstyle route based responder
    return route_responder(responder_result)


def route_responder(controller):
    """route_responder implements the responder paradigm for Routes
    based action dispatch
    
    In the event that the controller references something that is
    itself a valid rseponder, that responder will be returned directly
    and not wrapped.
    
    The RouteResponder handles calling the appropriate controller
    method given an action. It's initialized with a controller class
    which it will then initialized with a request object before calling
    the appropriate method on it. A wrapper is returned that implements
    the responder call-style.
    
    Methods wishing to terminate early may raise a webob HTTPException
    subclass which will be captured and passed up.
    
    Special methods you may define on your controller:
    
    ``_before``
        This method is called before your action is, and should be used
        for restricting access to other actions, or other tasks which
        may result in an HTTPException being thrown. Setup tasks should
        be done in your controller's ``__init__`` method.

    ``_after``
        This method is called after the action is, unless an unexpected
        exception was raised. Subclasses of
        :class:`~webob.exc.HTTPException` (such as those raised by
        ``redirect_to`` and ``abort``) are expected; e.g. ``__after__``
        will be called on redirects.
    
    The method will be called with no arguments.
    
    """
    # Record whether we have before/after to call
    before = hasattr(controller, '_before')
    after = hasattr(controller, '_after')
    
    # Find all the valid method's
    methods = dict(inspect.getmembers(controller, inspect.ismethod))
    
    def controller_wrapper(request):
        """The controller wrapper that is dispatched to by Pylons
        
        This wrapper implements the responder paradigm.
        
        """
        log_debug = request.environ['pylons.log_debug']
        
        # Instantiate the controller with the request
        controller_obj = controller(request)
        
        try:
            action_name = request.route_dict['action'].replace('-', '_')
        except KeyError:
            raise Exception("No action matched from Routes, unable to"
                            "determine action dispatch.")
        
        # Keep private methods private
        if action_name[0] == '_':
            if log_debug:
                log.debug("Action starts with _, private action not "
                          "allowed. Returning a 404 response")
            return HTTPNotFound()
        
        if log_debug:
            log.debug("Looking for %r method to handle the request", action_name)
        
        # Try and get the function to dispatch to
        if action_name in methods:
            action = methods[action_name]
        else:
            if log_debug:
                log.debug("Couldn't find %r method to handle response", action_name)
            if request.config['debug']:
                raise NotImplementedError('Action %r is not implemented' %
                                          action_name)
            else:
                return HTTPNotFound()
        
        # Call the before if its around, return if its an HTTPException
        if before:
            try:
                controller_obj._before()
            except HTTPException, httpe:
                return httpe
        
        try:
            response = action(controller_obj)
        except HTTPException, httpe:
            response = httpe
        except TypeError:
            # Raised when attempting to call a non-callable
            if log_debug:
                log.debug("Can't debug to non-callable action %r", action_name)
            response = HTTPNotFound()
        
        if after:
            controller_obj._after()
        return response
    return controller_wrapper


class WSGIController(object):
    """WSGI Controller that follows WSGI spec for calling and return
    values
    
    The Pylons WSGI Controller handles incoming web requests that are 
    dispatched from the PylonsBaseWSGIApp. These requests result in a
    new instance of the WSGIController being created, which is then
    called with the dict options from the Routes match. The standard
    WSGI response is then returned with start_response called as per
    the WSGI spec.
    
    Special WSGIController methods you may define:
    
    ``__before__``
        This method is called before your action is, and should be used
        for setting up variables/objects, restricting access to other
        actions, or other tasks which should be executed before the
        action is called.

    ``__after__``
        This method is called after the action is, unless an unexpected
        exception was raised. Subclasses of
        :class:`~webob.exc.HTTPException` (such as those raised by
        ``redirect_to`` and ``abort``) are expected; e.g. ``__after__``
        will be called on redirects.
        
    Each action to be called is inspected with :meth:`_inspect_call` so
    that it is only passed the arguments in the Routes match dict that
    it asks for. The arguments passed into the action can be customized
    by overriding the :meth:`_get_method_args` function which is
    expected to return a dict.
    
    In the event that an action is not found to handle the request, the
    Controller will raise an "Action Not Found" error if in debug mode,
    otherwise a ``404 Not Found`` error will be returned.
    
    """
    _pylons_log_debug = False

    def _perform_call(self, func, args):
        """Hide the traceback for everything above this method"""
        __traceback_hide__ = 'before_and_this'
        return func(**args)
    
    def _inspect_call(self, func):
        """Calls a function with arguments from
        :meth:`_get_method_args`
        
        Given a function, inspect_call will inspect the function args
        and call it with no further keyword args than it asked for.
        
        If the function has been decorated, it is assumed that the
        decorator preserved the function signature.
        
        """
        # Check to see if the class has a cache of argspecs yet
        try:
            cached_argspecs = self.__class__._cached_argspecs
        except AttributeError:
            self.__class__._cached_argspecs = cached_argspecs = {}
        
        try:
            argspec = cached_argspecs[func.im_func]
        except KeyError:
            argspec = cached_argspecs[func.im_func] = inspect.getargspec(func)
        kargs = self._get_method_args()
                
        log_debug = self._pylons_log_debug
        c = self._py_object.tmpl_context
        environ = self._py_object.request.environ
        args = None
        
        if argspec[2]:
            if self._py_object.config['pylons.tmpl_context_attach_args']:
                for k, val in kargs.iteritems():
                    setattr(c, k, val)
            args = kargs
        else:
            args = {}
            argnames = argspec[0][isinstance(func, types.MethodType)
                                  and 1 or 0:]
            for name in argnames:
                if name in kargs:
                    if self._py_object.config['pylons.tmpl_context_attach_args']:
                        setattr(c, name, kargs[name])
                    args[name] = kargs[name]
        if log_debug:
            log.debug("Calling %r method with keyword args: **%r",
                      func.__name__, args)
        try:
            result = self._perform_call(func, args)
        except HTTPException, httpe:
            if log_debug:
                log.debug("%r method raised HTTPException: %s (code: %s)",
                          func.__name__, httpe.__class__.__name__,
                          httpe.wsgi_response.code, exc_info=True)
            result = httpe
            
            # Store the exception in the environ
            environ['pylons.controller.exception'] = httpe
            
            # 304 Not Modified's shouldn't have a content-type set
            if result.wsgi_response.status_int == 304:
                result.wsgi_response.headers.pop('Content-Type', None)
            result._exception = True

        return result
    
    def _get_method_args(self):
        """Retrieve the method arguments to use with inspect call
        
        By default, this uses Routes to retrieve the arguments,
        override this method to customize the arguments your controller
        actions are called with.
        
        This method should return a dict.
        
        """
        req = self._py_object.request
        kargs = req.environ['pylons.routes_dict'].copy()
        kargs['environ'] = req.environ
        kargs['start_response'] = self.start_response
        kargs['pylons'] = self._py_object
        return kargs
    
    def _dispatch_call(self):
        """Handles dispatching the request to the function using
        Routes"""
        log_debug = self._pylons_log_debug
        req = self._py_object.request
        try:
            action = req.environ['pylons.routes_dict']['action']
        except KeyError:
            raise Exception("No action matched from Routes, unable to"
                            "determine action dispatch.")
        action_method = action.replace('-', '_')
        if log_debug:
            log.debug("Looking for %r method to handle the request",
                      action_method)
        try:
            func = getattr(self, action_method, None)
        except UnicodeEncodeError:
            func = None
        if action_method != 'start_response' and callable(func):
            # Store function used to handle request
            req.environ['pylons.action_method'] = func
            
            response = self._inspect_call(func)
        else:
            if log_debug:
                log.debug("Couldn't find %r method to handle response", action)
            if pylons.config['debug']:
                raise NotImplementedError('Action %r is not implemented' %
                                          action)
            else:
                response = HTTPNotFound()
        return response
    
    def __call__(self, environ, start_response):
        """The main call handler that is called to return a response"""
        log_debug = self._pylons_log_debug
                
        # Keep a local reference to the req/response objects
        self._py_object = environ['pylons.pylons']

        # Keep private methods private
        try:
            if environ['pylons.routes_dict']['action'][:1] in ('_', '-'):
                if log_debug:
                    log.debug("Action starts with _, private action not "
                              "allowed. Returning a 404 response")
                return HTTPNotFound()(environ, start_response)
        except KeyError:
            # The check later will notice that there's no action
            pass

        start_response_called = []
        def repl_start_response(status, headers, exc_info=None):
            response = self._py_object.response
            start_response_called.append(None)
            
            # Copy the headers from the global response
            if log_debug:
                log.debug("Merging pylons.response headers into "
                          "start_response call, status: %s", status)
            headers.extend(header for header in response.headerlist
                           if header[0] == 'Set-Cookie' or
                           header[0].startswith('X-'))
            return start_response(status, headers, exc_info)
        self.start_response = repl_start_response
        
        if hasattr(self, '__before__'):
            response = self._inspect_call(self.__before__)
            if hasattr(response, '_exception'):
                return response(environ, self.start_response)
        
        response = self._dispatch_call()
        if not start_response_called:
            self.start_response = start_response
            py_response = self._py_object.response
            # If its not a WSGI response, and we have content, it needs to
            # be wrapped in the response object
            if isinstance(response, str):
                if log_debug:
                    log.debug("Controller returned a string "
                              ", writing it to pylons.response")
                py_response.body = py_response.body + response
            elif isinstance(response, unicode):
                if log_debug:
                    log.debug("Controller returned a unicode string "
                              ", writing it to pylons.response")
                py_response.unicode_body = py_response.unicode_body + \
                        response
            elif hasattr(response, 'wsgi_response'):
                # It's an exception that got tossed.
                if log_debug:
                    log.debug("Controller returned a Response object, merging "
                              "it with pylons.response")
                for name, value in py_response.headers.items():
                    if name.lower() == 'set-cookie':
                        response.headers.add(name, value)
                    else:
                        response.headers.setdefault(name, value)
                try:
                    registry = environ['paste.registry']
                    registry.replace(pylons.response, response)
                except KeyError:
                    # Ignore the case when someone removes the registry
                    pass
                py_response = response
            elif response is None:
                if log_debug:
                    log.debug("Controller returned None")
            else:
                if log_debug:
                    log.debug("Assuming controller returned an iterable, "
                              "setting it as pylons.response.app_iter")
                py_response.app_iter = response
            response = py_response
        
        if hasattr(self, '__after__'):
            after = self._inspect_call(self.__after__)
            if hasattr(after, '_exception'):
                after.wsgi_response = True
                response = after
        
        if hasattr(response, 'wsgi_response'):
            # Copy the response object into the testing vars if we're testing
            if 'paste.testing_variables' in environ:
                environ['paste.testing_variables']['response'] = response
            if log_debug:
                log.debug("Calling Response object to return WSGI data")
            
            # Emit the NewResponse event
            self._py_object.config.events.publish(NewResponse(response))
            
            return response(environ, self.start_response)
        
        if log_debug:
            log.debug("Response assumed to be WSGI content, returning "
                      "un-touched")
        return response

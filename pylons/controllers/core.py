"""The core WSGIController"""
import inspect
import logging
import types
import warnings

from paste.httpexceptions import HTTPException
from paste.response import HeaderDict
from paste.wsgiwrappers import WSGIResponse

import pylons

__all__ = ['Controller', 'WSGIController']

log = logging.getLogger(__name__)

class WSGIController(object):
    """WSGI Controller that follows WSGI spec for calling and return values
    
    The Pylons WSGI Controller handles incoming web requests that are 
    dispatched from the PylonsBaseWSGIApp. These requests result in a new 
    instance of the WSGIController being created, which is then called with the
    dict options from the Routes match. The standard WSGI response is then
    returned with start_response called as per the WSGI spec.
    
    By default, the WSGIController will search and attempt to call a 
    ``__before__`` method before calling the action, and will try to call a
    ``__after__`` method after the action was called. These two methods can act
    as filters controlling access to the action, setup variables/objects for 
    use with a set of actions, etc.
    
    Each action to be called is inspected with ``_inspect_call`` so that it is
    only passed the arguments in the Routes match dict that it asks for. The
    arguments passed into the action can be customized by overriding the 
    ``_get_method_args`` function which is expected to return a dict.
    
    In the event that an action is not found to handle the request, the
    Controller will raise an "Action Not Found" error if in debug mode,
    otherwise a ``404 Not Found`` error will be returned.
    """
    
    __pudge_all__ = ['_inspect_call', '__call__', '_get_method_args', 
                     '_dispatch_call']
    _pylons_log_debug = False
    
    def _inspect_call(self, func):
        """Calls a function with arguments from ``_get_method_args``
        
        Given a function, inspect_call will inspect the function args and call
        it with no further keyword args than it asked for.
        
        If the function has been decorated, it is assumed that the decorator
        preserved the function signature.
        """
        argspec = inspect.getargspec(func)
        kargs = self._get_method_args()
        log_debug = self._pylons_log_debug
        
        # Hide the traceback for everything above this controller
        __traceback_hide__ = 'before_and_this'
        
        c = pylons.c._current_obj()
        args = None
        if argspec[2]:
            for k, val in kargs.iteritems():
                setattr(c, k, val)
            args = kargs
        else:
            args = {}
            argnames = argspec[0][1:]
            for name in argnames:
                if name in kargs:
                    setattr(c, name, kargs[name])
                    args[name] = kargs[name]
        if log_debug:
            log.debug("Calling %r method with keyword args: **%r",
                      func.__name__, args)
        try:
            result = func(**args)
        except HTTPException, httpe:
            if log_debug:
                log.debug("%r method raised HTTPException: %s (code: %s)",
                          func.__name__, httpe.__class__.__name__, httpe.code,
                          exc_info=True)
            result = httpe.response(pylons.request.environ)
            result._exception = True
        return result
    
    def _get_method_args(self):
        """Retrieve the method arguments to use with inspect call
        
        By default, this uses Routes to retrieve the arguments, override
        this method to customize the arguments your controller actions are
        called with.
        """
        req = pylons.request._current_obj()
        kargs = req.environ['pylons.routes_dict'].copy()
        kargs['environ'] = req.environ
        if hasattr(self, 'start_response'):
            kargs['start_response'] = self.start_response
        return kargs
    
    def _dispatch_call(self):
        """Handles dispatching the request to the function using Routes"""
        log_debug = self._pylons_log_debug
        req = pylons.request._current_obj()
        action = req.environ['pylons.routes_dict'].get('action')
        action_method = action.replace('-', '_')
        if log_debug:
            log.debug("Looking for %r method to handle the request",
                      action_method)
        try:
            func = getattr(self, action_method, None)
        except UnicodeEncodeError:
            func = None
        if isinstance(func, types.MethodType):
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
                response = WSGIResponse(code=404)
        return response
    
    def __call__(self, environ, start_response):
        log_debug = self._pylons_log_debug

        # Keep private methods private
        if environ['pylons.routes_dict'].get('action', '')[:1] in ('_', '-'):
            if log_debug:
                log.debug("Action starts with _, private action not allowed. "
                          "Returning a 404 response")
            return WSGIResponse(code=404)(environ, start_response)

        start_response_called = []
        def repl_start_response(status, headers, exc_info=None):
            response = pylons.response._current_obj()
            start_response_called.append(None)
            
            # Copy the headers from the global response
            # XXX: TODO: This should really be done with a more efficient 
            #            header merging function at some point.
            if log_debug:
                log.debug("Merging pylons.response headers into "
                          "start_response call, status: %s", status)
            response.headers.update(HeaderDict.fromlist(headers))
            headers = response.headers.headeritems()
            for c in pylons.response.cookies.values():
                headers.append(('Set-Cookie', c.output(header='')))
            return start_response(status, headers, exc_info)
        self.start_response = repl_start_response
        
        if hasattr(self, '__before__'):
            response = self._inspect_call(self.__before__)
            if hasattr(response, '_exception'):
                return response(environ, self.start_response)
        
        response = self._dispatch_call()
        if not start_response_called:
            # If its not a WSGI response, and we have content, it needs to
            # be wrapped in the response object
            if hasattr(response, 'wsgi_response'):
                # It's either a legacy WSGIResponse object, or an exception
                # that got tossed.
                if log_debug:
                    log.debug("Controller returned a Response object, merging "
                              "it with pylons.response")
                response.headers.update(pylons.response.headers)
                for c in pylons.response.cookies.values():
                    response.headers.add('Set-Cookie', c.output(header=''))
                registry = environ['paste.registry']
                registry.replace(pylons.response, response)
            elif isinstance(response, types.GeneratorType):
                if log_debug:
                    log.debug("Controller returned a generator, setting it as "
                              "the pylons.response content")
                pylons.response.content = response
            elif response is None:
                if log_debug:
                    log.debug("Controller returned None")
            else:
                if log_debug:
                    log.debug("Assuming controller returned a basestring or "
                              "buffer, writing it to pylons.response")
                pylons.response.write(response)
            response = pylons.response._current_obj()
        
        if hasattr(self, '__after__'):
            after = self._inspect_call(self.__after__)
            if hasattr(after, '_exception'):
                return after(environ, self.start_response)
        
        if hasattr(response, 'wsgi_response'):
            # Copy the response object into the testing vars if we're testing
            if 'paste.testing_variables' in environ:
                environ['paste.testing_variables']['response'] = response
            if log_debug:
                log.debug("Calling Response object to return WSGI data")
            return response(environ, self.start_response)
        
        if log_debug:
            log.debug("Response assumed to be WSGI content, returning un-touched")
        return response


class Controller(WSGIController):
    """Deprecated Pylons Controller for Web Requests
    
    All Pylons projects should use the WSGIController.
    """
    def __init__(self, *args, **kwargs):
        warnings.warn("Controller class is deprecated, switch to using the"
                      "WSGIController class", DeprecationWarning, 2)
        WSGIController.__init__(self, *args, **kwargs)
    
    def __call__(self, *args, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        """
        req = pylons.request._current_obj()
        
        # Keep private methods private
        if req.environ['pylons.routes_dict'].get('action', '').startswith('_'):
            return WSGIResponse(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)
        response = self._dispatch_call()
        
        # If its not a WSGI response, and we have content, it needs to
        # be wrapped in the response object
        if hasattr(response, 'wsgi_response'):
            # It's either a legacy WSGIResponse object, or an exception
            # that got tossed. Strip headers if its anything other than a
            # 2XX status code, and strip cookies if its anything other than
            # a 2XX or 3XX status code.
            if response.status_code < 300:
                response.headers.update(pylons.response.headers)
            if response.status_code < 400:
                for c in pylons.response.cookies.values():
                    response.headers.add('Set-Cookie', c.output(header=''))
            registry = req.environ['paste.registry']
            registry.replace(pylons.response, response)
        elif isinstance(response, types.GeneratorType):
            pylons.response.content = response
        elif isinstance(response, basestring):
            pylons.response.write(response)
        response = pylons.response._current_obj()
        
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__)
        
        return response

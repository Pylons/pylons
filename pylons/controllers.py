"""Standard Controllers intended for sub-classing by web developers"""
import types
import inspect
import xmlrpclib

from paste.deploy.config import CONFIG
from paste.deploy.converters import asbool

import pylons

class Controller(object):
    """Standard Pylons Controller for Web Requests
    
    The Pylons Controller handles incoming web requests that are dispatched
    from the custom Myghty Routes resolver. These requests result in a new
    instance of the Controller being created, which is then called with the
    dict options from the Routes match.
    
    By default, the Controller will search and attempt to call a ``__before__``
    method before calling the action, and will try to call a ``__after__``
    method after the action was called. These two methods can act as filters
    controlling access to the action, setup variables/objects for use with a
    set of actions, etc.
    
    Each action to be called is inspected with ``_inspect_call`` so that it is
    only passed the arguments in the Routes match dict that it asks for. The only
    exception to the dict is that the Myghty ``ARGS`` variable is included.
    
    In the event that an action is not found to handle the request, the Controller
    will raise an "Action Not Found" error if in debug mode, otherwise a ``404 Not Found``
    error will be returned.
    
    """
    __pudge_all__ = ['_inspect_call', '__call__', '_attach_locals']
    
    def _attach_locals(self):
        """Attach Pylons special objects to the controller
        
        When debugging, the Pylons special objects are unavailable because they
        are thread locals. This function pulls the actual object and attaches it
        to the controller so that it can be examined for debugging purposes.
        
        """
        self.c = pylons.c._current_obj()
        self.g = pylons.g._current_obj()
        self.cache = pylons.cache._current_obj()
        self.session = pylons.session._current_obj()
        self.request = pylons.request._current_obj()
        self.buffet = pylons.buffet._current_obj()
    
    def _inspect_call(self, func, **kargs):
        """Calls a function with the Routes dict
        
        Given a function, inspect_call will inspect the function args and call
        it with no further keyword args than it asked for.
        
        If the function has been decorated, it is assumed that the decorator
        preserved the function signature.
        
        """
        argspec = inspect.getargspec(func)
        kargs = self._req.environ['pylons.routes_dict'].copy()
        
        # @@ LEGACY: Add in ARGS alias to params
        if self._req.environ.get('pylons.legacy'):
            kargs['ARGS'] = self._req._legacy_params
        
        c = pylons.c._current_obj()
        if argspec[2]:
            for k,v in kargs.iteritems(): setattr(c, k, v)
            return func(**kargs)
        else:
            argnames = argspec[0][1:]
            args = []
            for name in argnames:
                if kargs.has_key(name):
                    setattr(c, name, kargs[name])
                    args.append(kargs[name])
            return func(*args)
    
    def _dispatch_call(self):
        """Handles dispatching the request to the function"""
        action = self._req.environ['pylons.routes_dict'].get('action')
        action_method = action.replace('-', '_')
        func = getattr(self, action_method, None)
        if isinstance(func, types.MethodType):
            response = self._inspect_call(func)
        else:
            if asbool(CONFIG['global_conf'].get('debug')):
                raise NotImplementedError('Action %s is not implemented' % action)
            else:
                response = pylons.Response(code=404)
        return response
    
    def __call__(self, *args, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        
        """
        self._req = pylons.request._current_obj()
        
        # Keep private methods private
        if self._req.environ['pylons.routes_dict'].get('action').startswith('_'):
            return pylons.Response(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)
        response = self._dispatch_call()
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__)
        return response

class WSGIController(Controller):
    """WSGI Controller that follows WSGI spec for calling and return values
    
    This function works identically to the normal Controller, however it is called
    with the WSGI interface, and behaves as a WSGI application calling start_response
    and returning an iterable as content.
    
    """
    def __call__(self, environ, start_response):
        self.start_response = start_response
        match = environ['pylons.routes_dict']
        self._req = pylons.request._current_obj()
        
        # Keep private methods private
        if match.get('action').startswith('_'):
            return pylons.Response(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__)
        response = self._dispatch_call()
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__)
        
        if hasattr(response, 'wsgi_response'):
            # Pull the content we need for a WSGI response
            status, response_headers, content = response.wsgi_response()
            start_response(status, response_headers)
        
            # Copy the response object into the testing vars if we're testing
            if environ.get('paste.testing'):
                environ['paste.testing_variables']['response'] = response
            response = content
        
        return response
        

class RPCController(Controller):
    resource = 'RPC2'

    def __call__(self, environ, start_response):


        self.start_response = start_response
        match = environ['pylons.routes_dict']
        self._req = pylons.request._current_obj()
        
        # Keep private methods private
        if match.get('action').startswith('_'):
            return pylons.Response(code=404)

        if  match.get('action') != RPCController.resource:
            if environ['paste.config']['global_conf']['debug'] == 'false':
                return pylons.Response(code=404)
            else:
                raise NotImplementedError('RPCController only supports %s action', RPCController.resource) 
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__)
        response = pylons.Response(xmlrpclib.dumps(( self._dispatch_call().wsgi_response()[2] ,)))
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__)
        return response


    
    def __call__2(self, action, **kargs):
        self._req = pylons.request._current_obj()
        action = self._req.environ['pylons.routes_dict'].get('action')
        action_method = action.replace('-', '_')
        if action_method != RPCController.resource:
            if asbool(CONFIG['global_conf'].get('debug')):
                raise NotImplementedError('RPCController only supports %s action',
                                          RPCController.resource)
            else:
                return pylons.Response(code=404)
        d = self._req.environ['wsgi.input'].read()
        params, method = xmlrpclib.loads(d)
        
        if hasattr(self, '__before__'):
            self.__before__(method, **params)
        if isinstance(getattr(self, method, None), types.MethodType):
            self.__getattribute__(method)(**params)
        else:
            res = 3#supposed to return xmlrpc fault thing
        response = pylons.Response(xmlrpclib.dumps((res,)))
        if hasattr(self, '__after__'):
            self.__after__(pylons, method, **params)
        return response

__all__ = ['Controller', 'WSGIController', 'RPCController']

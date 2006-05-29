"""Standard Controllers intended for sub-classing by web developers"""
import types
import inspect
import xmlrpclib

from paste.deploy.config import CONFIG

import pylons
from paste.wsgiwrappers import WSGIResponse

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
        self.request = pylons.request.current_obj()
        self.session = pylons.session.current_obj()
        #self.buffet = pylons.buffet.current_obj()
        self.c = pylons.c.current_obj()
    
    def _inspect_call(self, func, **kargs):
        """Calls a function with the names in kargs
        
        Given a function, inspect_call will inspect the function args and call
        it with no further keyword args than it asked for.
        
        If the function has been decorated, the decorator should have ensured
        that the original function is available at _orig for introspection.
        """
        # Get original function if its decorated
        if hasattr(func, '_orig'):
            argspec = inspect.getargspec(func._orig)
        else:
            argspec = inspect.getargspec(func)
        kargs['ARGS'] = pylons.request.params
        if argspec[2]:
            return func(**kargs)
        else:
            argnames = argspec[0][1:]
            args = [kargs[name] for name in argnames if kargs.has_key(name)]
            return func(*args)
    
    def __call__(self, *args, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        
        """
        # This if statement is to deal with legacy apps
        if args:
            action = args[0]
            kargs['action'] = action
        else:
            action = kargs['action']
        
        action_method = action.replace('-', '_')
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)
        if isinstance(getattr(self, action_method, None), types.MethodType):
            func = getattr(self, action_method)
            response = self._inspect_call(func, **kargs)
        else:
            if CONFIG['global_conf']['debug'] == 'false':
                response = WSGIResponse(code=404)
            else:
                raise NotImplementedError('Action %s is not implemented'%action)
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__, **kargs)
        return response

class RPCController(Controller):
    resource = 'RPC2'
    
    def __call__(self, action, **kargs):
        if action != RPCController.resource:
            if CONFIG['default']['debug'] == 'false':
                pylons.m.abort(404, "File not found")
            else:
                raise NotImplementedError('RPCController only supports %s action', RPCController.resource)
        d = pylons.m.request_args['_file'].read()
        params, method = xmlrpclib.loads(d)
        
        if hasattr(self, '__before__'):
            self.__before__(method, **params)
        if isinstance(getattr(self, method, None), types.MethodType):
            self.__getattribute__(method)(**params)
        else:
            res = 3#supposed to return xmlrpc fault thing
        pylons.m.write(xmlrpclib.dumps((res,)))
        if hasattr(self, '__after__'):
            self.__after__(pylons, method, **params)

__all__ = ['Controller', 'RPCController']

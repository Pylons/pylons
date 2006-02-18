"""Standard Controllers intended for sub-classing by web developers"""
import types
import inspect
import xmlrpclib

from paste.deploy.config import CONFIG

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
        self.request = pylons.request._get_object()
        self.session = pylons.session._get_object()
        self.m = pylons.m._get_object()
        self.c = pylons.c.copy()
    
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
        if argspec[2]:
            func(**kargs)
        else:
            argnames = argspec[0][1:]
            args = [kargs[name] for name in argnames if kargs.has_key(name)]
            func(*args)
    
    def __call__(self, action, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        """
        kargs['action'] = action
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)
        if isinstance(getattr(self, kargs['action'], None), types.MethodType):
            func = getattr(self, kargs['action'])
            self._inspect_call(func, **kargs)
        else:
            if CONFIG['default']['debug'] == 'false':
                pylons.m.abort(404, "File not found")
            else:
                raise NotImplementedError('Action %s is not implemented'%action)
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__, **kargs)

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


class BricksController(Controller):
    """Allows Pylons applications to use Controllers from the Bricks framework
    
    Sets up a basic Bricks environment within Pylons to allow a Bricks
    controller to run in a Pylons app. Implements the Bricks ``self.view()`` 
    method via Buffet to support Cheetah templates in Pylons and supports
    the Bricks ``self.setup()`` via the Pylons contoller ``__before__()`` 
    method.
    
    All Cheetah templates must be in ``templates/cheetah_root`` and be 
    pre-compiled using the ``cheetah compile`` command.

    Does not support ``start_response()`` within the controller.
    """

    def view(self, template, namespace={}, format='cheetah'):
        if format == 'raw':
            path = '/'.join(__file__.replace('\\','/').split('/')[:-2])+'/templates/cheetah_root/%s.tmpl'%template
            fp = open(path,'r')
            data = fp.read()
            fp.close()
            return data
        else:
            if not namespace.has_key('environ'):
                namespace['environ']=request.environ
            if not namespace.has_key('title'):
                namespace['title']=''
            if not namespace.has_key('head'):
                namespace['head']=''
            return pylons.buffet.render('cheetah', template, namespace=namespace, as_string=True)
        
    def _write(self, template, data):
        path = '/'.join(__file__.replace('\\','/').split('/')[:-2])+'/templates/cheetah_root/%s.tmpl'%template
        fp = open(path,'w')
        fp.write(data)
        fp.close()
        
    def __call__(self, action, ARGS, **params):
        from pylons import m, request, buffet
        buffet.prepare('cheetah', '.'.join(__name__.split('.')[:-1])+'.templates.cheetah_root')
        cgi = {}
        class CGIFieldStorageEmulator:
            def __init__(self, value):
                self.value = value
        for k, arg in ARGS.items():
            if isinstance(arg, list):
                args_ =  []
                for arg_ in arg:
                    args_.append(CGIFieldStorageEmulator(arg_))
                cgi[k] = args_
            else:
                cgi[k] = CGIFieldStorageEmulator(arg)
        request.environ['web.cgi'] = cgi
        request.environ['bricks.app.url'] = pylons.util.get_prefix(request.environ)
        request.environ['bricks.app.public.url'] = pylons.util.get_prefix(request.environ)
        if self.__class__.__name__ not in ['ErrorController','TemplateController']:
            if hasattr(getattr(self, action),'expose') and getattr(self, action).expose != 0:
                data = Controller.__call__(self, action, **params)
                if data != None:
                    for d in data:
                        m.write(data)
            else:
                raise Exception('Not exposed %s'%action)
        else:
            Controller.__call__(self, action, **params)

__all__ = ['Controller', 'RPCController', 'BricksController']

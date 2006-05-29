"""REST decorators"""

import pylons
from pylons.decorator import decorator

def restrict(*methods):
    """Restricts access to the function depending on HTTP method"""
    def entangle(func):
        def check_methods(func, *args, **kw):
            if pylons.request.method not in methods:
                response = pylons.Response()
                response.headers['Allow'] = ','.join(methods)
                response.status_code = 405
                return response
            return func(*args, **kw)
        return check_methods
    return decorator(entangle)

def dispatch_on(**method_map):
    """Dispatches to alternate controller methods based on HTTP method
    
    Multiple keyword arguments should be passed, with the keyword corresponding
    to the HTTP method to dispatch on (DELETE, POST, GET, etc.) and the
    value being the function to call. The value should *not* be a string, but
    the actual function object that should be called.
    
    Example::
    
        class SomeController(BaseController):
            
            @pylons.rest.dispatch_on(POST='create_comment')
            def comment(self, id):
                # Do something with the comment
            
            def create_comment(self, id):
                # Do something if its a post to comment
    
    **Please Note:** Due to how the argument inspection process works for
    methods, any desired function args must be present in the decorated
    function for them to be available in the dispatched function. The
    dispatched method can however have less arguments than the decorated
    one.
    
    """
    def entangle(func):
        def dispatcher(func, self, *args, **kw):
            alt_method = method_map.get(pylons.request.method)
            if alt_method:
                alt_method = getattr(self, alt_method)
                return self._inspect_call(alt_method, **kw)
            return self.func(self, *args, **kw)
        return dispatcher
    return decorator(entangle)

__all__ = ['restrict', 'dispatch_on']

"""REST decorators"""

import pylons

def restrict(*methods):
    """Restricts access to the function depending on HTTP method"""
    def check_methods(func):
        def new_func(*args, **kw):
            pylons.response.headers['Allow'] = ','.join(methods)
            if pylons.request.method not in methods:
                pylons.response.status_code = 405
                return pylons.response
            return func(*args, **kw)
        new_func._orig = getattr(func, '_orig', func)
        return new_func
    return check_methods

def dispatch_on(**method_map):
    """Dispatches to alternate controller methods based on HTTP method
    
    Multiple keyword arguments should be passed, with the keyword corresponding
    to the HTTP method to dispatch on (DELETE, POST, GET, etc.) and the
    value being the function to call. The value should *not* be a string, but
    the actual function object that should be called.
    
    Example::
    
        class SomeController(BaseController):
            
            @pylons.rest.dispatch_in(POST=create_comment)
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
    def dispatcher(func):
        def new_func(self, *args, **kw):
            alt_method = method_map.get(pylons.request.method)
            if alt_method:
                alt_method = getattr(self, alt_method)
                return self._inspect_call(alt_method, **kw)
            return func(self, *args, **kw)
        new_func._orig = getattr(func, '_orig', func)
        return new_func
    return dispatcher

__all__ = ['restrict', 'dispatch_on']

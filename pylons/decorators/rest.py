"""REST decorators"""

import pylons
from pylons.decorator import decorator

def restrict(*methods):
    """Restricts access to the function depending on HTTP method
    
    Example:
    
    .. code-block:: Python
        
        class SomeController(BaseController):
            
            @pylons.rest.restrict('GET')
            def comment(self, id):
    
    """
    def check_methods(func, *args, **kw):
        if pylons.request.method not in methods:
            response = pylons.Response()
            response.headers['Allow'] = ','.join(methods)
            response.status_code = 405
            return response
        return func(*args, **kw)
    return decorator(check_methods)

def dispatch_on(**method_map):
    """Dispatches to alternate controller methods based on HTTP method
    
    Multiple keyword arguments should be passed, with the keyword corresponding
    to the HTTP method to dispatch on (DELETE, POST, GET, etc.) and the
    value being the function to call. The value should *not* be a string, but
    the actual function object that should be called.
    
    Example:
    
    .. code-block:: Python
    
        class SomeController(BaseController):
            
            @pylons.rest.dispatch_on(POST='create_comment')
            def comment(self):
                # Do something with the comment
            
            def create_comment(self, id):
                # Do something if its a post to comment
    
    """
    def dispatcher(func, self, *args, **kw):
        alt_method = method_map.get(pylons.request.method)
        if alt_method:
            alt_method = getattr(self, alt_method)
            return self._inspect_call(alt_method, **kw)
        return func(self, *args, **kw)
    return decorator(dispatcher)

__all__ = ['restrict', 'dispatch_on']

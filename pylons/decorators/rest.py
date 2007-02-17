"""REST decorators"""
from decorator import decorator

import pylons

def restrict(*methods):
    """Restricts access to the function depending on HTTP method
    
    Example:
    
    .. code-block:: Python
        
        from pylons.decorators import rest
        
        class SomeController(BaseController):
            
            @rest.restrict('GET')
            def comment(self, id):
    """
    def check_methods(func, *args, **kwargs):
        """Wrapper for restrict"""
        if pylons.request.method not in methods:
            response = pylons.Response()
            response.headers['Allow'] = ','.join(methods)
            response.status_code = 405
            return response
        return func(*args, **kwargs)
    return decorator(check_methods)

def dispatch_on(**method_map):
    """Dispatches to alternate controller methods based on HTTP method
    
    Multiple keyword arguments should be passed, with the keyword corresponding
    to the HTTP method to dispatch on (DELETE, POST, GET, etc.) and the
    value being the function to call. The value should be a string indicating
    the name of the function to dispatch to.
    
    Example:
    
    .. code-block:: Python
        
        from pylons.decorators import rest
        
        class SomeController(BaseController):
            
            @rest.dispatch_on(POST='create_comment')
            def comment(self):
                # Do something with the comment
            
            def create_comment(self, id):
                # Do something if its a post to comment
    """
    def dispatcher(func, self, *args, **kwargs):
        """Wrapper for dispatch_on"""
        alt_method = method_map.get(pylons.request.method)
        if alt_method:
            alt_method = getattr(self, alt_method)
            return self._inspect_call(alt_method, **kwargs)
        return func(self, *args, **kwargs)
    return decorator(dispatcher)

__all__ = ['restrict', 'dispatch_on']

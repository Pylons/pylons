"""Legacy objects for Pylons 0.8 projects"""
from paste.registry import StackedObjectProxy
import paste.httpexceptions as httpexceptions

import pylons
import pylons.helpers
import pylons.templating as tmpl

# Legacy objects
m = StackedObjectProxy(name="m legacy object")
params = StackedObjectProxy(name="params")

class Myghty_Compat(object):
    """Myghty Compatibility Object for Pylons 0.8 Projects"""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.headers_out = pylons.helpers.response.headers
        self.headers_in = pylons.request.headers
        self.request_args = pylons.request.params
    
    def write(self, content):
        pylons.helpers.response.write(content)
    
    def out(self, content):
        pylons.helpers.response.write(content)
    
    def cache_self(self, *args, **kargs):
        return False
    
    def subexec(self, *args, **kargs):
        pylons.helpers.response.write(tmpl.render(*args, **kargs))
    
    def comp(self, *args, **kargs):
        pylons.helpers.response.write(tmpl.render(fragment=True, *args, **kargs))
    
    def scomp(self, *args, **kargs):
        return tmpl.render(fragment=True, *args, **kargs)
    
    def fetch_component(self, name):
        return name
    
    def get_cache(self, component):
        return pylons.cache.get_cache(component)
    
    def send_redirect(self, path, hard=True):
        raise httpexceptions.HTTPFound(path)
    
    def abort(self, status_code=None, reason=""):
        if status_code == 404:
            raise httpexceptions.HTTPNotFound()
        else:
            exc = httpexceptions.get_exception(status_code)(detail=reason)
            raise exc

__all__ = ['m', 'params']

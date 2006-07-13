"""Myghty compatibility object, ``etag_cache``, ``redirect_to`` and Myghty Module Components

Additional helper object available for use in Controllers is the etag_cache, along with
the Myghty compatibility objects for Pylons 0.8 projects and new Myghty Module Components
for use in Myghty templates.

"""
from paste.registry import StackedObjectProxy
import paste.httpexceptions as httpexceptions
from formencode import htmlfill

import pylons
import pylons.helpers
import pylons.templating as tmpl

response = StackedObjectProxy(name="response")

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to a new response object and
    returned for use in your action.
    
    Suggested use is within a Controller Action like so::
    
        import pylons
        
        class YourController(BaseController):
            def index(self):
                resp = pylons.etag_cache(key=1)
                resp.write(render('/splash.myt'))
                return resp
    
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    resp = pylons.response()
    resp.headers['ETag'] = key
    if str(key) == if_none_match:
        raise httpexceptions.HTTPNotModified()
    else:
        return resp

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
        pylons.helpers.response.write(tmpl.render_fragment(*args, **kargs))
    
    def scomp(self, *args, **kargs):
        return tmpl.render_fragment(*args, **kargs)
    
    def fetch_component(self, name):
        return name
    
    def get_cache(self, component):
        return pylons.cache.get_cache(component)
    
    def send_redirect(self, path, hard=True):
        redirect_to(path)
    
    def abort(self, status_code=None, reason=""):
        if status_code == 404:
            raise httpexceptions.HTTPNotFound()
        else:
            exc = httpexceptions.get_exception(status_code)(detail=reason)
            raise exc

def redirect_to(url):
    """Redirect function to raise an httpexception causing a 302 Redirect"""
    raise httpexceptions.HTTPFound(url)

def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception
    
    In the event that the status_code is a 300 series error, the detail 
    attribute will be used as the Location header should one not be specified
    in the headers attribute.
    
    """
    exc = httpexceptions.get_exception(status_code)(detail, headers, comment)
    raise exc

__all__ = ['etag_cache', 'redirect_to', 'formfill']

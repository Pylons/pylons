"""Myghty compatibility object, ``etag_cache``, ``redirect_to`` and Myghty Module Components

Additional helper object available for use in Controllers is the etag_cache, along with
the Myghty compatibility objects for Pylons 0.8 projects and new Myghty Module Components
for use in Myghty templates.

"""
from routes import redirect_to
from paste.registry import StackedObjectProxy
import paste.httpexceptions as httpexceptions

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
                resp = etag_cache(key=1)
                resp.write(render('/splash.myt'))
                return resp
    
    .. Note:: 
        This works because etag_cache will raise an HTTPNotModified
        exception if the ETag recieved matches the key provided.
    
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    resp = pylons.Response()
    resp.headers['ETag'] = key
    if str(key) == if_none_match:
        raise httpexceptions.HTTPNotModified()
    else:
        return resp

def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception
    
    In the event that the status_code is a 300 series error, the detail 
    attribute will be used as the Location header should one not be specified
    in the headers attribute.
    
    """
    exc = httpexceptions.get_exception(status_code)(detail, headers, comment)
    raise exc

__all__ = ['etag_cache', 'redirect_to', 'formfill']

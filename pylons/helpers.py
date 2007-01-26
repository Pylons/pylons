"""``etag_cache``, ``redirect_to``, and ``abort`` methods

Additional helper object available for use in Controllers is the etag_cache.
"""
import paste.httpexceptions as httpexceptions

from routes import url_for

import pylons

def log(msg):
    """Log a message to the output log."""
    pylons.request.environ['wsgi.errors'].write('=> %s\n' % str(msg))

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to a new response object and
    returned for use in your action.
    
    Suggested use is within a Controller Action like so:
    
    .. code-block:: Python
    
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

def redirect_to(*args, **kargs):
    """Raises a redirect exception
    
    A Response object can be passed in as _response which will have the headers
    and cookies extracted from it and added into the redirect issued."""
    response = kargs.pop('_response', None)
    found = httpexceptions.HTTPFound(url_for(*args, **kargs))
    if response:
        if str(response.status_code).startswith('3'):
            found.code = response.status_code
        found.headers.extend(response.headers.headeritems())
        for c in response.cookies.values():
            found.headers.append(('Set-Cookie', c.output(header='')))
    raise found

__all__ = ['etag_cache', 'redirect_to', 'abort', 'log']

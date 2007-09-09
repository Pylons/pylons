"""Utility functions available for use by Controllers

``etag_cache``, ``redirect_to``, and ``abort``.
"""
import logging
import warnings

import paste.httpexceptions as httpexceptions

from routes import url_for

import pylons
import pylons.legacy

__all__ = ['abort', 'etag_cache', 'redirect_to']

log = logging.getLogger(__name__)

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to the response headers.
    
    Suggested use is within a Controller Action like so:
    
    .. code-block:: Python
    
        import pylons
        
        class YourController(BaseController):
            def index(self):
                etag_cache(key=1)
                return render('/splash.mako')
    
    .. Note:: 
        This works because etag_cache will raise an HTTPNotModified
        exception if the ETag recieved matches the key provided.
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    pylons.response.headers['ETag'] = key
    if str(key) == if_none_match:
        log.debug("ETag match, returning 304 HTTP Not Modified Response")
        raise httpexceptions.HTTPNotModified()
    else:
        log.debug("ETag didn't match, returning response object")
        return pylons.response


def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception
    
    In the event that the status_code is a 300 series error, the detail 
    attribute will be used as the Location header should one not be specified
    in the headers attribute.
    """
    exc = httpexceptions.get_exception(status_code)(detail, headers, comment)
    log.debug("Aborting request, status: %s, detail: %r, headers: %r, "
              "comment: %r", status_code, detail, headers, comment)
    raise exc


def redirect_to(*args, **kargs):
    """Raises a redirect exception
    
    Optionally, a _code variable may be passed with the status code of the 
    redirect, ie:

    .. code-block:: Python

        redirect_to('home_page', _code=303)
    
    ``Deprecated``
    A Response object can be passed in as _response which will have the headers
    and cookies extracted from it and added into the redirect issued."""
    response = kargs.pop('_response', None)
    status_code = kargs.pop('_code', 302)
    exc = httpexceptions.get_exception(status_code)
    found = exc(url_for(*args, **kargs))
    log.debug("Generating %s redirect" % status_code)
    if response:
        warnings.warn(pylons.legacy.redirect_response_warning,
                      PendingDeprecationWarning, 2)
        log.debug("Merging provided Response object into redirect")
        if str(response.status_code).startswith('3'):
            found.code = response.status_code
        for c in response.cookies.values():
            found.headers.add('Set-Cookie', c.output(header=''))
    raise found

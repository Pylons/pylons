"""Utility functions available for use by Controllers

``etag_cache``, ``redirect_to``, and ``abort``.
"""
import logging
import warnings

import paste.httpexceptions as httpexceptions
from routes import url_for
from webob import Request as WebObRequest
from webob import Response as WebObResponse
from webob.exc import status_map

import pylons
import pylons.legacy

__all__ = ['abort', 'etag_cache', 'redirect_to', 'Request', 'Response']

log = logging.getLogger(__name__)

class Request(WebObRequest):
    charset = 'utf-8'
    unicode_errors = 'replace'
    language = 'en-us'
    
    def determine_browser_charset(self):
        return self.accept_charset
    
    def languages(self):
        return self.accept_language.best_matches(self.language)
    languages = property(languages)
    
    def match_accept(self, mimetypes):
        return self.accept.first_match(mimetypes)


class Response(WebObResponse):
    default_content_type = 'text/html'
    errors = 'strict'
    content = WebObResponse.body
    
    def determine_charset(self):
        return self.charset
    
    def has_header(self, header):
        return header in self.headers
    
    def get_content(self):
        return self.body
    
    def write(self, content):
        self.body_file.write(content)
    
    def wsgi_response(self):
        return self.status, self.headers, self.body

    
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
        pylons.response.headers.pop('Content-Type', None)
        pylons.response.headers.pop('Cache-Control', None)
        pylons.response.headers.pop('Pragma', None)
        raise status_map[304]()
    else:
        log.debug("ETag didn't match, returning response object")
        return pylons.response


def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception
    
    In the event that the status_code is a 300 series error, the detail 
    attribute will be used as the Location header should one not be specified
    in the headers attribute.
    """
    exc = status_map[status_code](detail=detail, headers=headers, 
                                  comment=comment)
    log.debug("Aborting request, status: %s, detail: %r, headers: %r, "
              "comment: %r", status_code, detail, headers, comment)
    raise exc


def redirect_to(*args, **kargs):
    """Raises a redirect exception
    
    Optionally, a _code variable may be passed with the status code of the 
    redirect, ie:

    .. code-block:: Python

        redirect_to('home_page', _code=303)
    
    """
    response = kargs.pop('_response', None)
    status_code = kargs.pop('_code', 302)
    exc = status_map[status_code]
    found = exc(location=url_for(*args, **kargs))
    log.debug("Generating %s redirect" % status_code)
    raise found

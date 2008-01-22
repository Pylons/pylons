"""Utility functions available for use by Controllers

``etag_cache``, ``redirect_to``, and ``abort``.
"""
import logging
import mimetypes
import warnings

import paste.httpexceptions as httpexceptions
from routes import url_for
from webob import Request as WebObRequest
from webob import Response as WebObResponse
from webob.exc import status_map

import pylons

__all__ = ['abort', 'etag_cache', 'redirect_to', 'Request', 'Response']

log = logging.getLogger(__name__)

class Request(WebObRequest):
    """WebOb Request subclass
    
    The WebOb Request has no charset, or other defaults. This subclass
    adds defaults, along with several methods for backwards 
    compatibility with paste.wsgiwrappers.WSGIRequest.
    
    """
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
    """WebOb Response subclass
    
    The WebOb Response has no default content type, or error defaults.
    This subclass adds defaults, along with several methods for 
    backwards compatibility with paste.wsgiwrappers.WSGIResponse.
    
    """
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


class MIMETypes(object):
    """MIMETypes registration mapping
    
    The MIMETypes object class provides a single point to hold onto all
    the registered mimetypes, and their association extensions. It's
    used by the mimetypes function to determine the appropriat content
    type to return to a client.
    
    """
    extension_mapping = {}
    type_mapping = {}
    
    def load_defaults(cls):
        """Loads a default mapping of extensions and mimetypes
        
        These are suitable for most web applications by default. 
        Additional types can be added with the MIMETypes.register 
        method.
        
        """
        extension_mapping = {}
        type_mapping = {}
        mimetypes.init()
        for ext, mimetype in mimetypes.types_map.iteritems():
            type_mapping[mimetype] = ext[1:]
            extension_mapping[ext[1:]] = mimetype
        cls.extension_mapping.update(extension_mapping)
        cls.type_mapping.update(type_mapping)
        
        # Add some common defaults and aliases
        MIMETypes.register('*/*', 'all')
        MIMETypes.register('text/plain', 'text', ext_aliases=('txt',))
        MIMETypes.register('text/html', 'html', 
                           type_aliases=('application/xhtml+xml',), 
                           ext_aliases=('xhtml',))
        MIMETypes.register('text/javascript', 'js',
                           type_aliases=('application/javascript', 
                                         'application/x-javascript'))
        MIMETypes.register('text/css', 'css')
        MIMETypes.register('text/calendar', 'ics')
        MIMETypes.register('text/csv', 'csv')
        MIMETypes.register('application/xml', 'xml',
                           type_aliases=('text/xml', 'application/x-xml'))
        MIMETypes.register('application/rss+xml', 'rss')
        MIMETypes.register('application/atom+xml', 'atom')
        MIMETypes.register('application/x-yaml', 'yaml',
                           type_aliases=('text/yaml',))
        MIMETypes.register('multipart/form-data', 'multipart_form')
        MIMETypes.register('application/x-www-form-urlencoded', 'url_encoded_form')
        MIMETypes.register('application/json', 'json', 
                           type_aliases=('text/x-json',))
    load_defaults = classmethod(load_defaults)
    
    def register(cls, mimetype, extension, type_aliases=None, ext_aliases=None):
        """Register additional MIMETypes
        
        Additional mimetypes that a user wants to recognize and handle
        should be registered using this method. Extension aliases that
        should be treated as equivilant to the desired extension, along
        with alias mimetypes can also be registered.
        
        Example:
            # Register text/plain as the text extension, or txt
            MIMETypes.register('text/plain', 'text', ext_aliases=('txt',))
        
        """
        cls.type_mapping[mimetype] = extension
        if type_aliases:
            for alias in type_aliases:
                cls.type_mapping[alias] = extension
        
        cls.extension_mapping[extension] = mimetype
        if ext_aliases:
            for alias in ext_aliases:
                cls.extension_mapping[alias] = mimetype
    register = classmethod(register)


def mimetype(extension):
    """Check the Routes match and client HTTP Accept to attempt to use
    the appropriate mime-type
    
    This works best with Routes ``map.resource`` which sets up routes
    that can accept matches with a specific extension.
    
    Example:
        def somaction(self):
            # prepare a bunch of data
            # ......
            
            if mimetype('html'):
                return render('/some/template.html')
            elif mimetype('atom'):
                return render('/some/xml_template.xml')
            elif mimetype('csv'):
                # write the data to a csv file
                return csvfile
            else:
                abort(404)
    
    """
    request = pylons.request._current_obj()
    # Pull out the possible return content-type
    return_type = MIMETypes.extension_mapping.get(extension)
    if not return_type:
        raise Exception("Can't check for extensions that haven't been "
                        "registered")
    
    # Check for a format in Route args first
    route_format = request.environ['pylons.routes_dict'].get('format')
    if route_format:
        mime_type = MIMETypes.extension_mapping[route_format]
        resolved_extension = MIMETypes.type_mapping[mime_type]
        if resolved_extension == extension:
            pylons.response.headers['Content-Type'] = mime_type
            return True
    
    # Check to see if this matches in the Request accept
    if return_type in request.accept_language:
        pylons.response.headers['Content-Type'] = return_type
        return True
    
    # Didn't match the route format or the Request accept, don't match
    return False


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
    raise exc.exception


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
    raise found.exception

"""Utility functions and classes available for use by Controllers

Pylons subclasses the `WebOb <http://pythonpaste.org/webob/>`_
:class:`webob.Request` and :class:`webob.Response` classes to provide
backwards compatible functions for earlier versions of Pylons as well
as add a few helper functions to assist with signed cookies.

For reference use, refer to the :class:`Request` and :class:`Response`
below.

Functions available:

:func:`abort`, :func:`forward`, :func:`etag_cache`,
:func:`mimetype` and :func:`redirect`
"""
import base64
import binascii
import hmac
import logging
import re
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from hashlib import sha1
except ImportError:
    import sha as sha1

from webob import BaseRequest as WebObRequest
from webob import Response as WebObResponse
from webob.exc import status_map

import pylons

__all__ = ['abort', 'etag_cache', 'redirect', 'Request', 'Response']

log = logging.getLogger(__name__)

IF_NONE_MATCH = re.compile('(?:W/)?(?:"([^"]*)",?\s*)')


class Request(WebObRequest):
    """WebOb Request subclass

    The WebOb :class:`webob.Request` has no charset, or other defaults. This subclass
    adds defaults, along with several methods for backwards
    compatibility with paste.wsgiwrappers.WSGIRequest.

    """
    def determine_browser_charset(self):
        """Legacy method to return the
        :attr:`webob.Request.accept_charset`"""
        return self.accept_charset

    def languages(self):
        # And we now have the old best_matches code that webob ditched!
        al = self.accept_language
        try:
            items = [i for i, q in sorted(al._parsed, key=lambda iq: -iq[1])]
            for index, item in enumerate(items):
                if al._match(item, self.language):
                    items[index:] = [self.language]
                    break
            else:
                items.append(self.language)
            return items
        except AttributeError:
            # If its a NilAccept, there won't be a _parsed attribute
            # Return the best match instead
            return [self.accept_language.best_match(self.language)]
    languages = property(languages)

    def match_accept(self, mimetypes):
        return self.accept.first_match(mimetypes)

    def signed_cookie(self, name, secret):
        """Extract a signed cookie of ``name`` from the request

        The cookie is expected to have been created with
        ``Response.signed_cookie``, and the ``secret`` should be the
        same as the one used to sign it.

        Any failure in the signature of the data will result in None
        being returned.

        """
        cookie = self.str_cookies.get(name)
        if not cookie:
            return None
        try:
            input_sig, pickled = cookie[:40], base64.standard_b64decode(cookie[40:])
        except binascii.Error:
            # Badly formed data can make base64 die
            return None
        sig = hmac.new(secret, pickled, sha1).hexdigest()

        # Avoid timing attacks
        invalid_bits = 0
        if len(sig) != len(input_sig):
            return None

        for a, b in zip(sig, input_sig):
            invalid_bits += a != b

        if invalid_bits:
            return None
        else:
            return pickle.loads(pickled)


class Response(WebObResponse):
    """WebOb Response subclass

    The WebOb Response has no default content type, or error defaults.
    This subclass adds defaults, along with several methods for
    backwards compatibility with paste.wsgiwrappers.WSGIResponse.

    """
    content = WebObResponse.body

    def determine_charset(self):
        return self.charset

    def has_header(self, header):
        return header in self.headers

    def get_content(self):
        return self.body

    def wsgi_response(self):
        return self.status, self.headers, self.body

    def signed_cookie(self, name, data, secret=None, **kwargs):
        """Save a signed cookie with ``secret`` signature

        Saves a signed cookie of the pickled data. All other keyword
        arguments that ``WebOb.set_cookie`` accepts are usable and
        passed to the WebOb set_cookie method after creating the signed
        cookie value.

        """
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        sig = hmac.new(secret, pickled, sha1).hexdigest()
        self.set_cookie(name, sig + base64.standard_b64encode(pickled), **kwargs)


def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching

    If a "If-None-Match" header is found, and equivilant to ``key``,
    then a ``304`` HTTP message will be returned with the ETag to tell
    the browser that it should use its current cache of the page.

    Otherwise, the ETag header will be added to the response headers.

    Suggested use is within a Controller Action like so:

    .. code-block:: python

        import pylons

        class YourController(BaseController):
            def index(self):
                etag_cache(key=1)
                return render('/splash.mako')

    .. note::
        This works because etag_cache will raise an HTTPNotModified
        exception if the ETag received matches the key provided.

    """
    if_none_matches = IF_NONE_MATCH.findall(
        pylons.request.environ.get('HTTP_IF_NONE_MATCH', ''))
    response = pylons.response._current_obj()
    response.headers['ETag'] = '"%s"' % key
    if str(key) in if_none_matches:
        log.debug("ETag match, returning 304 HTTP Not Modified Response")
        response.headers.pop('Content-Type', None)
        response.headers.pop('Cache-Control', None)
        response.headers.pop('Pragma', None)
        raise status_map[304]()
    else:
        log.debug("ETag didn't match, returning response object")


def forward(wsgi_app):
    """Forward the request to a WSGI application. Returns its response.

    .. code-block:: python

        return forward(FileApp('filename'))

    """
    environ = pylons.request.environ
    controller = environ.get('pylons.controller')
    if not controller or not hasattr(controller, 'start_response'):
        raise RuntimeError("Unable to forward: environ['pylons.controller'] "
                           "is not a valid Pylons controller")
    return wsgi_app(environ, controller.start_response)


def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception

    In the event that the status_code is a 300 series error, the detail
    attribute will be used as the Location header should one not be
    specified in the headers attribute.

    """
    exc = status_map[status_code](detail=detail, headers=headers,
                                  comment=comment)
    log.debug("Aborting request, status: %s, detail: %r, headers: %r, "
              "comment: %r", status_code, detail, headers, comment)
    raise exc


def redirect(url, code=302):
    """Raises a redirect exception to the specified URL

    Optionally, a code variable may be passed with the status code of
    the redirect, ie::

        redirect(url(controller='home', action='index'), code=303)

    """
    log.debug("Generating %s redirect" % code)
    exc = status_map[code]
    raise exc(location=url.encode('utf-8'))

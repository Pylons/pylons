"""Security related decorators"""
import logging
import urlparse

from decorator import decorator
try:
    import webhelpers.html.secure_form as secure_form
except ImportError:
    import webhelpers.pylonslib.secure_form as secure_form
    

from pylons.controllers.util import abort, redirect
from pylons.decorators.util import get_pylons

__all__ = ['authenticate_form', 'https']

log = logging.getLogger(__name__)

csrf_detected_message = (
    "Cross-site request forgery detected, request denied. See "
    "http://en.wikipedia.org/wiki/Cross-site_request_forgery for more "
    "information.")

def authenticated_form(params):
    submitted_token = params.get(secure_form.token_key)
    return submitted_token is not None and \
        submitted_token == secure_form.authentication_token()


@decorator
def authenticate_form(func, *args, **kwargs):
    """Decorator for authenticating a form

    This decorator uses an authorization token stored in the client's
    session for prevention of certain Cross-site request forgery (CSRF)
    attacks (See
    http://en.wikipedia.org/wiki/Cross-site_request_forgery for more
    information).

    For use with the ``webhelpers.html.secure_form`` helper functions.

    """
    request = get_pylons(args).request
    if authenticated_form(request.POST):
        del request.POST[secure_form.token_key]
        return func(*args, **kwargs)
    else:
        log.warn('Cross-site request forgery detected, request denied: %r '
                 'REMOTE_ADDR: %s' % (request, request.remote_addr))
        abort(403, detail=csrf_detected_message)


def https(*redirect_args, **redirect_kwargs):
    """Decorator to redirect to the SSL version of a page if not
    currently using HTTPS. Apply this decorator to controller methods
    (actions).

    Takes a url argument: either a string url, or a callable returning a
    string url. The callable will be called with no arguments when the
    decorated method is called. The url's scheme will be rewritten to
    https if necessary.

    Non-HTTPS POST requests are aborted (405 response code) by this
    decorator.

    Example:

    .. code-block:: python

        # redirect to HTTPS /pylons
        @https('/pylons')
        def index(self):
            do_secure()

        # redirect to HTTPS /auth/login, delaying the url() call until
        # later (as the url object may not be functional when the
        # decorator/method are defined)
        @https(lambda: url(controller='auth', action='login'))
        def login(self):
            do_secure()

        # redirect to HTTPS version of myself
        @https()
        def get(self):
            do_secure()

    .. warning::

        Arguments as would be passed to the
        :func:`url_for`/:func:`redirect_to` functions are
        deprecated. Explicitly specify the url or a callable returning
        the url instead.

    """
    def wrapper(func, *args, **kwargs):
        """Decorator Wrapper function"""
        request = get_pylons(args).request
        if request.scheme.lower() == 'https':
            return func(*args, **kwargs)
        if request.method.upper() == 'POST':
            # don't allow POSTs (raises an exception)
            abort(405, headers=[('Allow', 'GET')])

        if redirect_kwargs:
            # XXX: not a foolproof check for url_for arguments, but the
            # best we can do
            import warnings
            from routes import url_for
            warnings.warn('Calling https with url_for args is deprecated, use '
                          'https(lambda: url(*args, **kwargs)) instead',
                          DeprecationWarning, 2)
            redirect_kwargs['protocol'] = 'https'
            url = url_for(*redirect_args, **redirect_kwargs)
        elif not redirect_args:
            url = request.url
        else:
            url = redirect_args[0]
            if callable(url):
                url = url()
        # Ensure an https scheme, which also needs a host
        parts = urlparse.urlparse(url)
        url = urlparse.urlunparse(('https', parts[1] or request.host) +
                                  parts[2:])

        log.debug('Redirecting non-https request: %s to: %s',
                  request.path_info, url)
        redirect(url)
    return decorator(wrapper)

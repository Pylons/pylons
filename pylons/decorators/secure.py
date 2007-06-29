"""Security related decorators"""
import logging
from decorator import decorator
log = logging.getLogger('pylons.decorators.secure')

from webhelpers.rails.secure_form_tag import authentication_token, token_key

from pylons import request, Response
from pylons.helpers import abort, redirect_to

csrf_detected_message = (
    "Cross-site request forgery detected, request denied. See "
    "http://en.wikipedia.org/wiki/Cross-site_request_forgery for more "
    "information.")

def authenticated_form(params):
    submitted_token = params.get(token_key)
    return submitted_token is not None and \
        submitted_token == authentication_token()

def authenticate_form(func, *args, **kwargs):
    """Decorator for authenticating a form according to an authorization token
    stored in the client's session. For prevention of certain Cross-site
    request forgery (CSRF) attacks (See
    http://en.wikipedia.org/wiki/Cross-site_request_forgery for more
    information).

    For use with the ``webhelpers.rails.secure_form_tag`` helper functions.
    """
    if authenticated_form(request.POST):
        del request.POST[token_key]
        return func(*args, **kwargs)
    else:
        log.debug('Cross-site request forgery detected, request denied: %r' %
                  request)
        return Response(csrf_detected_message, code=403)
authenticate_form = decorator(authenticate_form)

def https(*redirect_args, **redirect_kwargs):
    """Decorator to redirect to the SSL version of a page if not currently
    using HTTPS. Takes as arguments the parameters to pass to redirect_to.
    (Specify no arguments necessary to redirect the current page).  Apply this
    decorator to controller methods (actions).

    Non-https POST requests are aborted (405 response code) by this decorator.
    
    Example:
    
    .. code-block: Python
    
    @https('/pylons') # redirect to HTTPS /pylons
    def index(self):
        ...
        
    @https(controller='auth', action='login') # redirect to HTTPS /auth/login
    def login(self):
        ...

    @https() # redirect to HTTPS version of myself
    def get(self):
        ...
    """
    def wrapper(func, *args, **kwargs):
        """Decorator Wrapper function"""
        if request.scheme.lower() == 'https':
            return func(*args, **kwargs)
        else:
            if request.method.upper() != 'POST':
                redirect_kwargs['protocol'] = 'https' # ensure https
                redirect_to(*redirect_args, **redirect_kwargs)
            else:
                abort(405) # don't allow POSTs.
    return decorator(wrapper)

__all__ = ['authenticate_form', 'https']

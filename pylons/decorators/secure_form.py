"""Decorator for authenticating a form according to an authorization token
stored in the client's session. For prevention of Cross-site request forgery
(CSRF) attacks (See http://en.wikipedia.org/wiki/Cross-site_request_forgery for
more information).

For use with the ``webhelpers.rails.secure_form_tag`` helper functions.
"""
import logging
from decorator import decorator
log = logging.getLogger('pylons.decorators.secure_form')

from webhelpers.rails.secure_form_tag import authentication_token, token_key

from pylons import request, Response

denied_message = (
    "Cross-site request forgery detected, request denied. See "
    "http://en.wikipedia.org/wiki/Cross-site_request_forgery for more "
    "information.")

def authenticated_form(params):
    submitted_token = params.get(token_key)
    return submitted_token is not None and \
        submitted_token == authentication_token()

def authenticate_form(func, *args, **kw):
    """Action decorator that, with secure_form, prevents certain cross-site
    scripting attacks.
    """
    if authenticated_form(request.POST):
        del request.POST[token_key]
        return func(*args, **kw)
    else:
        log.debug('Cross-site request forgery detected, request denied: %r' %
                  request)
        return Response(denied_message, code=403)
authenticate_form = decorator(authenticate_form)

__all__ = ['authenticate_form']

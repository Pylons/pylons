"""Custom Decorators, currently ``jsonify``"""

import pylons
import simplejson as json

def jsonify(func):
    """Action decorator that formats output for JSON
    
    Given a function that will return content, this decorator will
    turn the result into JSON, with a content-type of 'text/javascript'
    and output it.
    """
    def decorator(*args, **kw):
        pylons.request.content_type = 'text/javascript'
        return pylons.m.write(json.dumps(func(*args, **kw)))
    if not hasattr(func, '_orig'):
        decorator._orig = func
    return decorator

__all__ = ['jsonify']

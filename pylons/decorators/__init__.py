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
        pylons.response.headers['Content-Type'] = 'text/javascript'
        pylons.response.content.append(json.dumps(func(*args, **kw)))
        return pylons.response
    decorator._orig = getattr(func, '_orig', func)
    return decorator

__all__ = ['jsonify']

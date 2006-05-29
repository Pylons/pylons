"""Custom Decorators, currently ``jsonify``"""
import simplejson as json
import pylons
from pylons.decorator import weak_signature_decorator

def jsonify(func):
    """Action decorator that formats output for JSON
    
    Given a function that will return content, this decorator will
    turn the result into JSON, with a content-type of 'text/javascript'
    and output it.
    """
    def decorator(*args, **kw):
        response = pylons.Response()
        response.headers['Content-Type'] = 'text/javascript'
        response.content.append(json.dumps(func(*args, **kw)))
        return response
    return weak_signature_decorator(decorator)

__all__ = ['jsonify']

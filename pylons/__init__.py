"""Base objects to be exported for use in Controllers"""
from paste.registry import StackedObjectProxy

from pylons.config import config
from pylons.legacy import h, jsonify

__all__ = ['app_globals', 'c', 'g', 'cache', 'request', 'response', 'session',
           'tmpl_context', 'jsonify']

def __figure_version():
    try:
        from pkg_resources import require
        import os
        # NOTE: this only works when the package is either installed,
        # or has an .egg-info directory present (i.e. wont work with raw
        # SVN checkout)
        info = require('pylons')[0]
        if os.path.dirname(os.path.dirname(__file__)) == info.location:
            return info.version
        else:
            return '(not installed)'
    except:
        return '(not installed)'
        
__version__ = __figure_version()

app_globals = g = StackedObjectProxy(name="G")
cache = StackedObjectProxy(name="Cache")
request = StackedObjectProxy(name="Request")
response = StackedObjectProxy(name="Response")
session = StackedObjectProxy(name="Session")
tmpl_context = c = StackedObjectProxy(name="C")

buffet = StackedObjectProxy(name="Buffet")
translator = StackedObjectProxy(name="Translator")

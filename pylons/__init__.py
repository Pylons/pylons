"""Base objects to be exported for use in Controllers"""
from paste.registry import StackedObjectProxy

from pylons.config import config
from pylons.legacy import h, jsonify, Controller, Response

__all__ = ['c', 'g', 'cache', 'request', 'response', 'session', 'jsonify',
           'Controller', 'Response']

def __figure_version():
    try:
        from pkg_resources import require
        import os
        # NOTE: this only works when the package is either installed,
        # or has an .egg-info directory present (i.e. wont work with raw SVN checkout)
        info = require('pylons')[0]
        if os.path.dirname(os.path.dirname(__file__)) == info.location:
            return info.version
        else:
            return '(not installed)'
    except:
        return '(not installed)'
        
__version__ = __figure_version()

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")

cache = StackedObjectProxy(name="Cache")
request = StackedObjectProxy(name="Request")
response = StackedObjectProxy(name="Response")
session = StackedObjectProxy(name="Session")

buffet = StackedObjectProxy(name="Buffet")
translator = StackedObjectProxy(name="Translator")

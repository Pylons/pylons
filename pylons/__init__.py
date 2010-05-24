"""Base objects to be exported for use in Controllers"""
# Import pkg_resources first so namespace handling is properly done so the
# paste imports work
import pkg_resources

from paste.registry import StackedObjectProxy

from pylons.configuration import config

__all__ = ['app_globals', 'cache', 'config', 'request', 'response',
           'session', 'tmpl_context', 'url']

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

app_globals = StackedObjectProxy(name="app_globals")
cache = StackedObjectProxy(name="cache")
request = StackedObjectProxy(name="request")
response = StackedObjectProxy(name="response")
session = StackedObjectProxy(name="session")
tmpl_context = StackedObjectProxy(name="tmpl_context or C")
url = StackedObjectProxy(name="url")

translator = StackedObjectProxy(name="translator")

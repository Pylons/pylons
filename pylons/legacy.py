"""Legacy functionality for pre Pylons 0.9.3 projects
"""
import sys
import types
import warnings

from paste.registry import StackedObjectProxy

import pylons
import pylons.decorators
from pylons.controllers import Controller as OrigController
from pylons.util import deprecated, func_move

default_charset_warning = (
"The 'default_charset' keyword argument to the %(klass)s constructor is "
"deprecated. Please specify response_settings=dict(charset='%(charset)s') to "
"""the Config constructor in your 'config/environment.py file instead, e.g.:\n
    return pylons.config.Config(tmpl_options, map, paths,
                                response_settings=dict(charset='%(charset)s'))"
""")

helpers_and_g_warning = (
"Pylons 0.9.3 and above now explicitly pass helpers and g "
"references to the PylonsApp constructor. Please update your "
"""middleware.py with:

    import %(package)s.lib.app_globals as app_globals
    import %(package)s.lib.helpers

Then edit the PylonsApp instantiation with:

    app = pylons.wsgiapp.PylonsApp(config, helpers=%(package)s.lib.helpers,
                                   g=app_globals.Globals)
""")

prefix_warning = (
"The [app:main] 'prefix' configuration option has been deprecated, please use "
"paste.deploy.config.PrefixMiddleware instead. To enable PrefixMiddleware in "
"""the config file, add the following line to the [app:main] section:

    filter-with = app-prefix

and the following lines to the end of the config file:

    [filter:app-prefix]
    use = egg:PasteDeploy#prefix
    prefix = %s
""")

pylons_h_warning = (
"pylons.h is deprecated: use your project's lib.helpers module directly "
"""instead. Your lib/helpers.py may require the following additional imports:

    from pylons.helpers import log
    from pylons.i18n import get_lang, set_lang

Use the following in your project's lib/base.py file (and any other module that
uses h):

    import MYPROJ.lib.helpers as h

(where MYPROJ is the name of your project) instead of:

    from pylons import h
""")


def load_h(package_name):
    """
    This is a legacy test for pre-0.9.3 projects to continue using the old
    style Helper imports. The proper style is to pass the helpers module ref
    to the PylonsApp during initialization.
    """
    __import__(package_name + '.lib.base')
    their_h = getattr(sys.modules[package_name + '.lib.base'], 'h', None)
    if isinstance(their_h, types.ModuleType):
        # lib.base.h is a module (and thus not pylons.h) -- assume lib.base
        # uses new style (self contained) helpers via:
        # import ${package}.lib.helpers as h
        return their_h

    # Assume lib.base.h is a StackedObjectProxy -- lib.base is using pre 0.9.2
    # style helpers via:
    # from pylons import h
    helpers_name = package_name + '.lib.helpers'
    __import__(helpers_name) 
    helpers_module = sys.modules[helpers_name]

    # Pre 0.9.2 lib.helpers did not import the pylons helper functions,
    # manually add them. Don't overwrite user functions (allowing pylons
    # helpers to be overridden)
    for func_name, func in {'_': pylons.i18n._, 'log': pylons.helpers.log,
                            'set_lang': pylons.i18n.set_lang,
                            'get_lang': pylons.i18n.get_lang}.iteritems():
        if not hasattr(helpers_module, func_name):
            setattr(helpers_module, func_name, func)

    return sys.modules[helpers_name]

jsonify = deprecated(pylons.decorators.jsonify,
                     func_move('pylons.jsonify',
                               moved_to='pylons.decorators.jsonify'))

controller_warning = ('pylons.Controller has been moved to '
                      'pylons.controllers.Controller.')
class Controller(OrigController):
    def __init__(self, *args, **kwargs):
        warnings.warn(controller_warning, DeprecationWarning, 2)
        OrigController.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        warnings.warn(controller_warning, DeprecationWarning, 2)
        return OrigController.__call__(self, *args, **kwargs)

class DeprecatedStackedObjectProxy(StackedObjectProxy):
    def _current_obj(*args, **kwargs):
        warnings.warn(pylons_h_warning, DeprecationWarning, 3)
        return StackedObjectProxy._current_obj(*args, **kwargs)
h = DeprecatedStackedObjectProxy(name="h")

__all__ = ['load_h']

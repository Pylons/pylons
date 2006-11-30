"""Legacy functionality for pre Pylons 0.9.3 projects
"""
import types
import sys
import warnings

import pylons

def load_h(package_name):
    """
    This is a legacy test for pre-0.9.3 projects to continue using the old
    style Helper imports. The proper style is to pass the helpers module ref
    to the PylonsApp during initialization.
    """
    warnings.warn(
        "Pylons 0.9.3 and above now passes the helpers module reference in "
        "directly. It's highly recommended that you update your middleware.py "
        "module so that the Pylons app load looks similar to:\n\n"
        "app = pylons.wsgiapp.PylonsApp(config, helpers=MYPROJ.lib.helpers, "
        "g=app_globals.Globals)\n\n"
        "Where MYPROJ is the name of your project. Also make sure to add an "
        "import line to the middleware.py to import the helpers modules:\n\n"
        "import MYPROJ.lib.helpers\n\n"
        "This will be required on all projects 1.0 and beyond.",
        DeprecationWarning, 2)
    __import__(package_name + '.lib.base')
    their_h = getattr(sys.modules[package_name + '.lib.base'], 'h', None)
    if isinstance(their_h, types.ModuleType):
        # lib.base.h is a module (and thus not pylons.h) -- assume lib.base uses
        # new style (self contained) helpers via:
        # import ${package}.lib.helpers as h
        return their_h

    # Assume lib.base.h is a StackedObjectProxy -- lib.base is using pre 0.9.2
    # style helpers via:
    # from pylons import h
    helpers_name = package_name + '.lib.helpers'
    __import__(helpers_name) 
    helpers_module = sys.modules[helpers_name]

    # Pre 0.9.2 lib.helpers did not import the pylons helper functions, manually
    # add them. Don't overwrite user functions (allowing pylons helpers to be
    # overridden)
    for func_name in ('_', 'log', 'set_lang', 'get_lang'):
        if not hasattr(helpers_module, func_name):
            setattr(helpers_module, func_name, getattr(pylons.util, func_name))

    return sys.modules[helpers_name]

__all__ = ['load_h']


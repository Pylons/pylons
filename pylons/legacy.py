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
    for func_name, func in {'_': pylons.i18n._, 'log': pylons.helpers.log,
                            'set_lang': pylons.i18n.set_lang,
                            'get_lang': pylons.i18n.get_lang}.iteritems():
        if not hasattr(helpers_module, func_name):
            setattr(helpers_module, func_name, func)

    return sys.modules[helpers_name]

__all__ = ['load_h']


"""Paste Template and Pylons utility functions

PylonsTemplate is a Paste Template sub-class that configures the source
directory and default plug-ins for a new Pylons project. The minimal template
provides a more minimal template with less additional directories and layout.
"""
import logging
import warnings

from paste.script.appinstall import Installer
from paste.script.templates import Template

import pylons
import pylons.configuration
import pylons.i18n

__all__ = ['AttribSafeContextObj', 'ContextObj', 'Helpers',
           'class_name_from_module_name', 'log', '_', 'set_lang', 'get_lang']
__pudge_all__ = __all__ + ['MinimalPylonsTemplate', 'PylonsTemplate']

pylons_log = logging.getLogger(__name__)

def func_move(name, moved_to='pylons.i18n'):
    return ("The %s function has moved to %s, please update your import "
            "statements to reflect the move" % (name, moved_to))


def deprecated(func, message):
    def deprecated_method(*args, **kargs):
        warnings.warn(message, DeprecationWarning, 2)
        return func(*args, **kargs)
    try:
        deprecated_method.__name__ = func.__name__
    except TypeError: # Python < 2.4
        pass
    deprecated_method.__doc__ = message + "\n\n" + func.__doc__
    return deprecated_method


get_lang = deprecated(pylons.i18n.get_lang, func_move('get_lang'))
set_lang = deprecated(pylons.i18n.set_lang, func_move('set_lang'))
_ = deprecated(pylons.i18n._, func_move('_'))

# Avoid circular import and a double warning
def log(*args, **kwargs):
    """Deprecated: Use the logging module instead.

    Log a message to the output log.
    """
    import pylons.helpers
    return pylons.helpers.log(*args, **kwargs)

def get_prefix(environ, warn=True):
    """Deprecated: Use environ.get('SCRIPT_NAME', '') instead"""
    if warn:
        warnings.warn("The get_prefix function is deprecated, please use "
                      "environ.get('SCRIPT_NAME', '') instead",
                      DeprecationWarning, 2)
    prefix = pylons.config.get('prefix', '')
    if not prefix:
        if environ.get('SCRIPT_NAME', '') != '':
            prefix = environ['SCRIPT_NAME']
    return prefix


def class_name_from_module_name(module_name):
    """Takes a module name and returns the name of the class it defines.

    If the module name contains dashes, they are replaced with underscores.

    Example::

        >>> class_name_from_module_name('with-dashes')
        'WithDashes'
        >>> class_name_from_module_name('with_underscores')
        'WithUnderscores'
        >>> class_name_from_module_name('oneword')
        'Oneword'
    """
    words = module_name.replace('-', '_').split('_')
    return ''.join([w.title() for w in words])


class ContextObj(object):
    """The 'c' object, with strict attribute access (raises an Exception when
    the attribute does not exist)"""
    def __repr__(self):
        attrs = [(name, value)
                 for name, value in self.__dict__.items()
                 if not name.startswith('_')]
        attrs.sort()
        parts = []
        for name, value in attrs:
            value_repr = repr(value)
            if len(value_repr) > 70:
                value_repr = value_repr[:60] + '...' + value_repr[-5:]
            parts.append(' %s=%s' % (name, value_repr))
        return '<%s.%s at %s%s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
            ','.join(parts))


class AttribSafeContextObj(ContextObj):
    """The 'c' object, with lax attribute access (returns '' when the attribute
    does not exist)"""
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pylons_log.debug("No attribute called %s found on c object, "
                             "returning empty string", name)
            return ''


class PylonsTemplate(Template):
    _template_dir = 'templates/default_project'
    summary = 'Pylons application template'
    egg_plugins = ['Pylons', 'WebHelpers']

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        package_logger = vars['package']
        if package_logger == 'root':
            # Rename the app logger in the rare case a project is named 'root'
            package_logger = 'app'
        vars['package_logger'] = package_logger

        template_engine = \
            vars.setdefault('template_engine',
                            pylons.configuration.default_template_engine)

        if template_engine == 'mako':
            # Support a Babel extractor default for Mako
            vars['babel_templates_extractor'] = \
                "('templates/**.mako', 'mako', None),\n%s#%s" % (' ' * 4,
                                                                 ' ' * 8)
        else:
            vars['babel_templates_extractor'] = ''

class MinimalPylonsTemplate(PylonsTemplate):
    _template_dir = 'templates/minimal_project'
    summary = 'Pylons minimal application template'


class PylonsInstaller(Installer):
    use_cheetah = False

"""Helpers object, Paste Template config and misc. functionality.

The util module provides the main Helper object used by Pylons.

PylonsTemplate is a Paste Template sub-class that configures the source
directory and default plug-ins for a new Pylons project.
"""
import os.path
from paste.deploy.config import CONFIG
from paste.script.templates import Template
import pylons

def log(msg):
    """Log a message to the output log."""
    pylons.request.environ['wsgi.errors'].write('=> %s\n'%str(msg))

def _(value):
    """Mark a string for translation
    
    Mark a string to be internationalized as follows:
    
    .. code-block:: Python
    
        h._('This should be in lots of languages')
    """
    return pylons.translator['translator'].gettext(value)

def set_lang(lang):
    """Set the language used"""
    if lang is None:
        pylons.translator['translator'] = _Translator()
    else:
        from pkg_resources import resource_exists
        from pylons.i18n.translation import egg_translation
        project_name = CONFIG['app_conf']['package']
        catalog_path = os.path.join('i18n', lang, 'LC_MESSAGES')
        if not resource_exists(project_name, catalog_path):
            raise LanguageError('Language catalog %s not found' % \
                                os.path.join(project_name, catalog_path))
        pylons.translator['translator'] = \
            egg_translation(project_name, lang=catalog_path)

def get_lang():
    return pylons.translator.get('lang')

def get_prefix(environ):
    if 'paste.config' in environ:
        prefix = environ['paste.config']['app_conf'].get('prefix', '')
    else:
        # Not ideal but if the error occurs before the paste.config is available not a lot we can do
        prefix = ''
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
    """ The 'c' object, with strict attribute access (raises an Exception when
    the attribute does not exist) """
    pass

class AttribSafeContextObj(object):
    """ The 'c' object, with lax attribute access (returns '' when the attribute
    does not exist) """
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return ''

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

class _Translator(object):
    """An empty gettext translator which just returns the original string"""
    def gettext(self, value):
        return value

class PylonsTemplate(Template):
    _template_dir = 'templates/default_project'
    summary = 'Pylons application template'
    egg_plugins = ['Pylons', 'WebHelpers']

class MinimalPylonsTemplate(Template):
    _template_dir = 'templates/minimal_project'
    summary = 'Pylons minimal application template'
    egg_plugins = ['Pylons', 'WebHelpers']
    

__all__ = ['AttribSafeContextObj', 'ContextObj', 'Helpers', 'class_name_from_module_name',
    'log', '_', 'set_lang', 'get_lang']
__pudge_all__ = __all__ + ['PylonsTemplate']

"""Helpers object, RequestLocal object, and Paste Template config

The util module provides the main Helper object used by Pylons.

The RequestLocal thread-local is utilized by Pylons as the ``c`` object that
is available via ``pylons.c`` and is cleared every request by Pylons.

PylonsTemplate is a Paste Template sub-class that configures the source
directory and default plug-ins for a new Pylons project.
"""
import sys
import os.path, gettext

from paste.script.templates import Template

import pylons

from routes import threadinglocal
from paste.deploy.config import CONFIG

def get_prefix(environ):
    prefix = environ['paste.config']['app_conf'].get('prefix', '')
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


class RequestLocal(object):
    """This object emulates a dict and supports the full set of dict functions
    and operations.
    
    Internally, the dict is attached to a threading local object and
    all access is passed through to the thread-safe object.
    
    This difference means that the object must be initialized per-thread
    with a _clear() call before the object can be used, and it should be
    _clear()'ed every request call.
    
    The RequestLocal object also support attribute assignment, which is
    then internally stored as if they used item assignment. Attribute
    get is also supported, and is used to 'get' the name requested. Unlike
    normal attribute access, this will return an empty string if the
    attribute does not exist.
    """
    def __init__(self):
        self.__dict__['_local'] = threadinglocal.local()
        
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            try:
                result = getattr(self._local.request, name)
            except AttributeError:
                result = self._local.request.get(name, '')
            return result
    
    def __setattr__(self, key, value):
        if key.startswith('_'):
            raise AttributeError("You cannot set attributes begining with '_' \
on  the 'temp' object use temp['%s'] instead"%key)
            #object.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)
    
    def __len__(self):
        return self._local.request.__len__()
    
    def __getitem__(self, key):
        return self._local.request.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._local.request.__setitem__(key, value)
    
    def __delitem__(self, key):
        self._local.request.__delitem__(key)
    
    def __iter__(self):
        return self._local.request.__iter__()
    
    def __contains__(self, item):
        return self._local.request.__contains__(item)
    
    def _clear(self):
        self._local.request = {}
    
    def __repr__(self):
        return self._local.request.__repr__()

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

class _Translator(object):
    """An empty gettext translator which just returns the original string"""
    def gettext(self, value):
        return value

class Helpers(object):
    def __init__(self, **_pylons):
        self.__dict__['_local'] = RequestLocal()
        self.__dict__['_pylons'] = _pylons
    
    def __call__(self):
        """Initialize Helpers object for request with helpers module/object
        
        When called, the Helpers object will return itself, after initializing
        itself for the current thread/request. It is intended to be run at the
        begginning of every request to clear the thread local it uses and setup
        the helpers space that will be used for fetching helper names as well
        as translation.
        """
        self.__dict__['_local']._clear()
        project_name = CONFIG['app_conf']['package']
        try:
            helpers_name = project_name + '.config.helpers'
            __import__(helpers_name)
        except:
            helpers_name = project_name + '.lib.helpers'
            __import__(helpers_name)
        helpers = sys.modules[helpers_name]
        self.__dict__['_local'].helpers = helpers
        self.__dict__['_local'].translator = _Translator()
        self.__dict__['_local'].config = CONFIG
        if CONFIG['app_conf'].has_key('lang'):
            self.set_lang(CONFIG['app_conf']['lang'])
        else:
            self.__dict__['_local'].lang = None
        return self
        
    def __getattr__(self, name):
        if hasattr(self.__dict__['_local'].helpers, name):
            return getattr(self.__dict__['_local'].helpers, name)
        elif name in self.__dict__['_local'].keys() and name != '_local' and \
            len(str(name))>0 and str(name)[0] != '_':
            return getattr(self.__dict__['_local'],name)
        else:
            raise AttributeError('No such helper %s'%repr(name))
    
    def __setattr__(self, name, value):
        if name not in ['lang']:
            raise AttributeError("Helper attributes cannot be set. You should \
use the context object 'c' to store conext information.")
        else:
            self.set_lang(value)

    def log(self, msg):
        """Log a message to the output log."""
        pylons.request.environ['wsgi.errors'].write('=> %s\n'%str(msg))

    def translate(self, value):
        """Deprecated, use _()"""
        raise NotImplementedError('Use h._() instead')

    def _(self, value):
        """Mark a string for translation
        
        Mark a string to be internationalised as follows:
        
        .. code-block:: Python
        
            h._('This should be in lots of langauges')
        
        """
        return self.__dict__['_local'].translator.gettext(value)
  
    def set_lang(self, lang):
        """Set the language used"""
        project_name = CONFIG['app_conf']['package']
        self.__dict__['_local'].lang = lang
        if lang is None:
            self.__dict__['_local'].translator = _Translator()
        else:
            from pkg_resources import resource_string, resource_stream, \
                resource_exists, resource_filename
            from pylons.i18n.translation import egg_translation
            catalog_path = os.path.join('i18n', lang, 'LC_MESSAGES')
            if not resource_exists(project_name, catalog_path):
                raise LanguageError('Langauge catalog %s not found' % \
                                    os.path.join(project_name, catalog_path))
            self.__dict__['_local'].translator = \
                egg_translation(project_name, lang=catalog_path)

    def get_lang(self):
        return self.__dict__['_local'].lang


class PylonsTemplate(Template):
    _template_dir = 'templates/paster_template'
    summary = 'Pylons application template'
    egg_plugins = ['Pylons', 'WebHelpers']

__all__ = ['RequestLocal', 'Helpers']
__pudge_all__ = ['RequestLocal', 'Helpers', 'PylonsTemplate']

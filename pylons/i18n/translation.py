"""Translation/Localization functions.

Provides ``gettext`` translation functions via an app's ``pylons.translator``
and get/set_lang for changing the language translated to."""

import os
from gettext import NullTranslations, translation

from pkg_resources import resource_exists, resource_stream

import pylons

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

def gettext_noop(value):
    """Mark a string for translation without translating it. Returns value.

    Used for global strings, e.g.:

    .. code-block:: Python

        foo = N_('Hello')

        class Bar:
            def __init__(self):
                self.local_foo = _(foo)

        h.set_lang('fr')
        assert Bar().local_foo == 'Bonjour'
        h.set_lang('es')
        assert Bar().local_foo == 'Hola'
        assert foo == 'Hello'
    """
    return value
N_ = gettext_noop

def gettext(value):
    """Mark a string for translation. Returns the localized string of value.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        gettext('This should be in lots of languages')
    """
    return pylons.translator.gettext(value)

def ugettext(value):
    """Mark a string for translation. Returns the localized unicode string of
    value.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        _('This should be in lots of languages')
    """
    return pylons.translator.ugettext(value)
_ = ugettext

def ngettext(singular, plural, n):
    """Mark a string for translation. Returns the localized string of the
    pluralized value.

    This does a plural-forms lookup of a message id. ``singular`` is used as
    the message id for purposes of lookup in the catalog, while ``n`` is used
    to determine which plural form to use. The returned message is a string.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        ngettext('There is %(num)d file here', 'There are %(num)d files here',
                 n) % {'num': n}
    """
    return pylons.translator.ngettext(singular, plural, n)

def ungettext(singular, plural, n):
    """Mark a string for translation. Returns the localized unicode string of
    the pluralized value.

    This does a plural-forms lookup of a message id. ``singular`` is used as
    the message id for purposes of lookup in the catalog, while ``n`` is used
    to determine which plural form to use. The returned message is a Unicode
    string.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        ungettext('There is %(num)d file here', 'There are %(num)d files here',
                  n) % {'num': n}
    """
    return pylons.translator.ungettext(singular, plural, n)

def _get_translator(lang, **kwargs):
    """Utility method to get a valid translator object from a language name"""
    import pylons.util as util
    rootdir = pylons.g.pylons_config.paths.get('root_path')
    localedir = os.path.join(rootdir, 'i18n')
    if not isinstance(lang, list):
        lang = [lang]
    try:
        translator = translation(util.config_get('package'), localedir,
                                 languages=lang, **kwargs)
    except IOError, ioe:
        raise LanguageError('IOError: %s' % ioe)
    translator.pylons_lang = lang
    return translator

def set_lang(lang, **kwargs):
    """Set the i18n language used"""
    registry = pylons.request.environ['paste.registry']
    if not lang:
        registry.replace(pylons.translator, NullTranslations())
    else:
        translator = _get_translator(lang, **kwargs)
        registry.replace(pylons.translator, translator)

def get_lang():
    """Return the current i18n language used"""
    return getattr(pylons.translator, 'pylons_lang', None)

def add_fallback(lang):
    """Add a fallback language from which words not matched in other languages
    will be translated to."""
    return pylons.translator.add_fallback(_get_translator(lang))

__all__ = ['gettext_noop', 'N_', 'gettext', 'ugettext', '_', 'ngettext',
           'ungettext', 'set_lang', 'get_lang', 'LanguageError']

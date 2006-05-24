import os
from gettext import *

from pkg_resources import resource_stream

def egg_translation(domain, lang):
    """
    This method doesn't do all the checking etc of the gettext.translation method
    but it seems to work.
    
    We can't just use gettext.translation because the .mo files might be in eggs
    """
    class_ = GNUTranslations
    return class_(resource_stream(domain, os.path.join(lang, '%s.mo' % domain)))

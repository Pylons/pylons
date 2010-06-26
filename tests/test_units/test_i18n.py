# -*- coding: utf-8 -*-
import os
import sys

from paste.fixture import TestApp

import pylons
from pylons.i18n.translation import *
from pylons.i18n.translation import lazify
from pylons.i18n.translation import _get_translator

from test_events import make_app

file_root = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(file_root, 'sample_controllers')
lang_setup = {'pylons.paths': {'root': root}, 'pylons.package': 'sample_controllers'}
sys.path.append(file_root)
pylons.translator._push_object(_get_translator(None, pylons_config=lang_setup))

foo = N_('Hello')

foo_now = gettext('Hello')
foo_later = lazy_gettext('Hello')
lots = _(u'This should be in lots of languages')
lazy_lots = lazy_ugettext(u'This should be in lots of languages')
lazy_multi = ngettext('There is %(num)d file here', 'There are %(num)d files here', 2)

glob_set = []

class TestI18N(object):
    def test_lazify(self):
        def show_str(st):
            return '%s%s' % (st, len(glob_set))
        lazy_show_str = lazify(show_str)
        result1 = lazy_show_str('fred')
        result2 = show_str('fred')
        assert str(result1) == str(result2)
        glob_set.append('1')
        assert str(result1) != str(result2)
    
    def test_noop(self):
        class Bar(object):
            def __init__(self):
                self.local_foo = _(foo)
        
        assert Bar().local_foo == 'Hello'
        
        t = set_lang('fr', set_environ=False, pylons_config=lang_setup)
        pylons.translator._push_object(t)
        assert Bar().local_foo == 'Bonjour'
        t = set_lang('es', set_environ=False, pylons_config=lang_setup)
        pylons.translator._push_object(t)
        assert Bar().local_foo == u'¡Hola!'
        assert foo == 'Hello'

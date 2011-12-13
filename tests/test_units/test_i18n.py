# -*- coding: utf-8 -*-
import os
import sys

from paste.fixture import TestApp

from __init__ import test_root

lang_setup = None


def setup_py_trans():
    global lang_setup
    import pylons
    from pylons.i18n.translation import _get_translator
    root = os.path.join(test_root, 'sample_controllers')
    lang_setup = {'pylons.paths': {'root': root}, 'pylons.package': 'sample_controllers'}
    sys.path.append(test_root)
    pylons.translator._push_object(_get_translator(None, pylons_config=lang_setup))

glob_set = []


class TestI18N(object):
    def setUp(self):
        setup_py_trans()

    def test_lazify(self):
        from pylons.i18n.translation import lazify

        def show_str(st):
            return '%s%s' % (st, len(glob_set))
        lazy_show_str = lazify(show_str)
        result1 = lazy_show_str('fred')
        result2 = show_str('fred')
        assert str(result1) == str(result2)
        glob_set.append('1')
        assert str(result1) != str(result2)

    def test_noop(self):
        import pylons
        from pylons.i18n.translation import _, N_, set_lang
        foo = N_('Hello')

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

from projectname.tests import *

class TestSampleController(TestController):
    def test_set_lang(self):
        self._test_set_lang('set_lang')

    def test_set_lang_pylonscontext(self):
        self._test_set_lang('set_lang_pylonscontext')

    def _test_set_lang(self, action):
        response = self.app.get(url(controller='sample', action=action, lang='ja'))
        assert u'\u8a00\u8a9e\u8a2d\u5b9a\u3092\u300cja\u300d\u306b\u5909\u66f4\u3057\u307e\u3057\u305f'.encode('utf-8') in response
        response = self.app.get(url(controller='sample', action=action, lang='fr'))
        assert 'Could not set language to "fr"' in response

    def test_detect_lang(self):
        response = self.app.get(url(controller='sample', action='i18n_index'), headers={
                'Accept-Language':'fr;q=0.6, en;q=0.1, ja;q=0.3'})
        # expect japanese fallback for nonexistent french.
        assert u'\u6839\u672c\u30a4\u30f3\u30c7\u30af\u30b9\u30da\u30fc\u30b8'.encode('utf-8') in response

    def test_no_lang(self):
        response = self.app.get(url(controller='sample', action='no_lang'))
        assert 'No language' in response
        assert 'No languages' in response

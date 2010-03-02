import os
import sys

import pylons
import pylons.configuration as configuration
from beaker.cache import CacheManager
from beaker.middleware import SessionMiddleware
from paste.fixture import TestApp
from paste.registry import RegistryManager
from paste.deploy.converters import asbool
from pylons import url
from pylons.decorators import jsonify
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes import Mapper
from routes.middleware import RoutesMiddleware
from routes.util import URLGenerator

from nose.tools import raises


def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=os.path.join(root, 'sample_controllers'), controllers=os.path.join(root, 'sample_controllers', 'controllers'))
    sys.path.append(root)

    config = configuration.pylons_config
    config.init_app(global_conf, app_conf, package='sample_controllers', paths=paths)
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.connect('/{controller}/{action}')
    config['routes.map'] = map
    
    class AppGlobals(object): pass
    config['pylons.app_globals'] = AppGlobals()
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    app = SessionMiddleware(app, config)

    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [401, 403, 404, 500])
    app = RegistryManager(app)

    app.config = config
    return app

class TestJsonifyDecorator(object):
    def setUp(self):
        self.app = TestApp(make_app({}))
        url._push_object(URLGenerator(configuration.pylons_config['routes.map'], {}))
    
    def test_basic_response(self):
        response = self.app.get('/hello/index')
        assert 'Hello World' in response
    
    def test_config(self):
        assert pylons.config == configuration.config

    @raises(AssertionError)
    def test_eval(self):
        app = TestApp(make_app(dict(debug='True')))
        app.get('/hello/oops', status=500, extra_environ={'paste.throw_errors': False})

    def test_set_lang(self):
        self._test_set_lang('set_lang')

    def test_set_lang_pylonscontext(self):
        self._test_set_lang('set_lang_pylonscontext')

    def _test_set_lang(self, action):
        response = self.app.get(url(controller='i18nc', action=action, lang='ja'))
        assert u'\u8a00\u8a9e\u8a2d\u5b9a\u3092\u300cja\u300d\u306b\u5909\u66f4\u3057\u307e\u3057\u305f'.encode('utf-8') in response
        response = self.app.get(url(controller='i18nc', action=action, lang='fr'))
        assert 'Could not set language to "fr"' in response

    def test_detect_lang(self):
        response = self.app.get(url(controller='i18nc', action='i18n_index'), headers={
                'Accept-Language':'fr;q=0.6, en;q=0.1, ja;q=0.3'})
        # expect japanese fallback for nonexistent french.
        assert u'\u6839\u672c\u30a4\u30f3\u30c7\u30af\u30b9\u30da\u30fc\u30b8'.encode('utf-8') in response

    def test_no_lang(self):
        response = self.app.get(url(controller='i18nc', action='no_lang'))
        assert 'No language' in response
        assert 'No languages' in response
    
    def test_langs(self):
        response = self.app.get(url(controller='i18nc', action='langs'), headers={
                'Accept-Language':'fr;q=0.6, en;q=0.1, ja;q=0.3'})
        assert "['fr', 'ja', 'en', 'en-us']" in response

import os
import re
import sys


from nose.tools import raises

from __init__ import test_root


def make_app(global_conf, full_stack=True, static_files=True, include_cache_middleware=False, attribsafe=False, **app_conf):
    import pylons
    import pylons.configuration as configuration
    from beaker.cache import CacheManager
    from beaker.middleware import SessionMiddleware, CacheMiddleware
    from nose.tools import raises
    from paste.registry import RegistryManager
    from paste.deploy.converters import asbool
    from pylons.decorators import jsonify
    from pylons.middleware import ErrorHandler, StatusCodeRedirect
    from pylons.wsgiapp import PylonsApp
    from routes import Mapper
    from routes.middleware import RoutesMiddleware
    
    paths = dict(root=os.path.join(test_root, 'sample_controllers'), controllers=os.path.join(test_root, 'sample_controllers', 'controllers'))

    config = configuration.pylons_config
    config.init_app(global_conf, app_conf, package='sample_controllers', paths=paths)
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.connect('/{controller}/{action}')
    map.connect('/test_func', controller='sample_controllers.controllers.hello:special_controller')
    map.connect('/test_empty', controller='sample_controllers.controllers.hello:empty_wsgi')
    config['routes.map'] = map
    
    class AppGlobals(object):
        def __init__(self):
            self.cache = 'Nothing here but a string'
    
    config['pylons.app_globals'] = AppGlobals()
    
    if attribsafe:
        config['pylons.strict_tmpl_context'] = False
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    if include_cache_middleware:
        app = CacheMiddleware(app, config)
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

class TestWsgiApp(object):
    def setUp(self):
        from paste.fixture import TestApp
        from routes.util import URLGenerator
        
        app = make_app({})
        self.app = TestApp(app)
        self.url = URLGenerator(app.config['routes.map'], {})
    
    def test_testvars(self):
        resp = self.app.get('/_test_vars', extra_environ={'paste.testing_variables': True})
        assert re.match(r'^\d+$', resp.body)
    
    def test_exception_resp_attach(self):
        resp = self.app.get('/test_func', expect_errors=True)
        assert resp.status == 404
    
    @raises(Exception)
    def test_no_content(self):
        resp = self.app.get('/test_empty', expect_errors=True)
        assert 'wontgethre'
    
    def test_middleware_cache_obj_instance(self):
        from paste.fixture import TestApp
        app = TestApp(make_app({}, include_cache_middleware=True))
        resp = app.get('/hello/index')
        assert resp.cache
    
    def test_attribsafe_tmpl_context(self):
        from paste.fixture import TestApp
        app = TestApp(make_app({}, attribsafe=True))
        resp = app.get('/hello/index')
        assert 'Hello World' in resp
    
    def test_cache_obj_appglobals(self):
        resp = self.app.get('/hello/index', extra_environ={'paste.testing_variables': True})
        assert resp.cache == 'Nothing here but a string'
    
    def test_controller_name_override(self):
        resp = self.app.get('/goodbye/index')
        assert 'Hello World' in resp


class TestJsonifyDecorator(object):
    def setUp(self):
        from paste.fixture import TestApp
        from routes.util import URLGenerator
        app = make_app({})
        self.config = app.config
        self.app = TestApp(app)
        self.url = URLGenerator(app.config['routes.map'], {})
    
    def test_basic_response(self):
        response = self.app.get('/hello/index')
        assert 'Hello World' in response
    
    def test_config(self):
        import pylons
        import pylons.configuration as configuration
        assert pylons.config == configuration.config

    @raises(AssertionError)
    def test_eval(self):
        from paste.fixture import TestApp
        app = TestApp(make_app(dict(debug='True')))
        app.get('/hello/oops', status=500, extra_environ={'paste.throw_errors': False})

    def test_set_lang(self):
        self._test_set_lang('set_lang')

    def test_set_lang_pylonscontext(self):
        self._test_set_lang('set_lang_pylonscontext')

    def _test_set_lang(self, action):
        response = self.app.get(self.url(controller='i18nc', action=action, lang='ja'))
        assert u'\u8a00\u8a9e\u8a2d\u5b9a\u3092\u300cja\u300d\u306b\u5909\u66f4\u3057\u307e\u3057\u305f'.encode('utf-8') in response
        response = self.app.get(self.url(controller='i18nc', action=action, lang='ch'))
        assert 'Could not set language to "ch"' in response

    def test_detect_lang(self):
        response = self.app.get(self.url(controller='i18nc', action='i18n_index'), headers={
                'Accept-Language':'fr;q=0.6, en;q=0.1, ja;q=0.3'})
        # expect japanese fallback for nonexistent french.
        assert u'\u6839\u672c\u30a4\u30f3\u30c7\u30af\u30b9\u30da\u30fc\u30b8'.encode('utf-8') in response

    def test_no_lang(self):
        response = self.app.get(self.url(controller='i18nc', action='no_lang'))
        assert 'No language' in response
        assert 'No languages' in response
    
    def test_langs(self):
        response = self.app.get(self.url(controller='i18nc', action='langs'), headers={
                'Accept-Language':'fr;q=0.6, en;q=0.1, ja;q=0.3'})
        assert "['fr', 'ja', 'en-us']" in response

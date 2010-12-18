import warnings

from paste.fixture import TestApp
from paste.registry import RegistryManager

from __init__ import TestWSGIController

def make_cache_controller_app():
    from pylons.testutil import ControllerWrap, SetupCacheGlobal
    from pylons.decorators import jsonify
    from pylons.controllers import WSGIController
    
    class CacheController(WSGIController):

        @jsonify
        def test_bad_json(self):
            return ["this is neat"]

        @jsonify
        def test_bad_json2(self):
            return ("this is neat",)
    
        @jsonify
        def test_good_json(self):
            return dict(fred=42)

    environ = {}
    app = ControllerWrap(CacheController)
    app = sap = SetupCacheGlobal(app, environ)
    app = RegistryManager(app)
    app = TestApp(app)
    return app, environ


class TestJsonifyDecorator(TestWSGIController):
    def setUp(self):
        self.app, environ = make_cache_controller_app()
        TestWSGIController.setUp(self)
        environ.update(self.environ)
        warnings.simplefilter('error', Warning)
    
    def tearDown(self):
        warnings.simplefilter('always', Warning)

    def test_bad_json(self):
        for action in 'test_bad_json', 'test_bad_json2':
            try:
                response = self.get_response(action=action)
            except Warning, msg:
                assert 'JSON responses with Array envelopes are' in msg[0]
    
    def test_good_json(self):
        response = self.get_response(action='test_good_json')
        assert '{"fred": 42}' in response
        assert response.header('Content-Type') == 'application/json; charset=utf-8'

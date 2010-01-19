import warnings

from paste.fixture import TestApp
from paste.registry import RegistryManager

import pylons
from pylons.decorators import jsonify
from pylons.controllers import WSGIController, XMLRPCController

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

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

class TestJsonifyDecorator(TestWSGIController):
    def setUp(self):
        self.app = app
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

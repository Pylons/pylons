from unittest import TestCase

from paste.wsgiwrappers import WSGIRequest

import pylons
from pylons import Controller
from pylons.util import ContextObj

class OldController(Controller):
    def index(self):
        return 'old'

class TestDeprecatedControllerImport(TestCase):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True))}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = OldController()
        self.controller.start_response = None

    def test_index(self):
        assert 'old' == self.controller()

from paste.fixture import TestApp
from paste.registry import RegistryManager

from pylons import jsonify
from pylons.decorators import jsonify as orig_jsonify
from pylons.controllers import WSGIController

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

class SimpleTestWSGIController(TestWSGIController):
    wsgi_app = None
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(self.wsgi_app)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron, setup_cache=False)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)

class JsonifyController(WSGIController):
    def index(self):
        return {'iam': 'deprecated'}
    index = jsonify(index)

class TestDeprecatedJsonify(SimpleTestWSGIController):
    wsgi_app = JsonifyController
    def test_wsgi_call(self):
        resp = self.get_response()
        assert '{"iam": "deprecated"}' in resp
        assert orig_jsonify.__doc__ in jsonify.__doc__

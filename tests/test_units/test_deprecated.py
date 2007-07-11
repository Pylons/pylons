import warnings
from unittest import TestCase

from paste.fixture import TestApp
from paste.registry import RegistryManager
from paste.wsgiwrappers import WSGIRequest

import pylons
from pylons import jsonify, Controller
from pylons.controllers import WSGIController
from pylons.decorators import jsonify as orig_jsonify
from pylons.util import ContextObj

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

class OldController(Controller):
    def index(self):
        return 'old'

class TestDeprecatedControllerImport(TestCase):
    def tearDown(self):
        warnings.simplefilter('always', DeprecationWarning)
    
    def test_index(self):
        warnings.simplefilter('error', DeprecationWarning)
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True))}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        try:
            self.controller = OldController()
        except DeprecationWarning, msg:
            assert 'pylons.Controller has been moved' in msg[0]

class SimpleTestWSGIController(TestWSGIController):
    wsgi_app = None
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(self.wsgi_app)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)

class JsonifyController(WSGIController):
    def index(self):
        return {'iam': 'deprecated'}

class TestDeprecatedJsonify(SimpleTestWSGIController):
    wsgi_app = JsonifyController
    
    def tearDown(self):
        warnings.simplefilter('always', DeprecationWarning)
    
    def test_wsgi_call(self):
        warnings.simplefilter('error', DeprecationWarning)
        try:
            self.wsgi_app.index = jsonify(self.wsgi_app.index)
            resp = self.get_response()
        except DeprecationWarning, msg:
            assert 'The pylons.jsonify function has moved to' in msg[0]
        #assert '{"iam": "deprecated"}' in resp
        #assert orig_jsonify.__doc__ in jsonify.__doc__

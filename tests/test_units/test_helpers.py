import warnings
from unittest import TestCase

from paste.fixture import TestApp
from paste.httpexceptions import HTTPMovedPermanently
from paste.registry import RegistryManager

import pylons
from pylons.controllers import WSGIController
from pylons.controllers.util import etag_cache
from pylons.decorators import jsonify as orig_jsonify
from pylons.util import ContextObj

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

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


class HelpersController(WSGIController):

    def test_etag_cache(self):
        etag_cache('test')
        return "from etag_cache"
    

class TestHelpers(SimpleTestWSGIController):
    wsgi_app = HelpersController

    def setUp(self):
        SimpleTestWSGIController.setUp(self)
        warnings.simplefilter('error', DeprecationWarning)

    def tearDown(self):
        SimpleTestWSGIController.tearDown(self)
        warnings.simplefilter('always', DeprecationWarning)

    def test_return_etag_cache(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'test_etag_cache'
        response = self.app.get('/')
        assert '"test"' == response.header('Etag')
        assert 'from etag_cache' in response

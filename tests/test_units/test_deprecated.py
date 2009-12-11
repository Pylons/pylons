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
    def imports(self):
        import pylons.controllers.util
        self.helpers = pylons.controllers.util

    def abort(self):
        self.helpers.abort(404)

    def etag_cache(self):
        self.helpers.etag_cache('hello')
        return 'etag cache'

    def redirect_to(self):
        self.helpers.redirect_to('/etag_cache')

class TestDeprecatedHelpers(SimpleTestWSGIController):
    wsgi_app = HelpersController()

    def setUp(self):
        warnings.simplefilter('ignore', DeprecationWarning)
        self.wsgi_app.imports()
        warnings.simplefilter('error', DeprecationWarning)
    
    def tearDown(self):
        warnings.simplefilter('always', DeprecationWarning)



class MiscLegacyController(WSGIController):

    def legacy_httpexception(self):
        raise HTTPMovedPermanently('/elsewhere')

    def legacy_etag_cache(self):
        # used to crash
        response = etag_cache('test')
        response.body = 'from etag_cache'
        return response


class TestMiscLegacy(SimpleTestWSGIController):
    wsgi_app = MiscLegacyController

    def setUp(self):
        SimpleTestWSGIController.setUp(self)
        warnings.simplefilter('error', DeprecationWarning)

    def tearDown(self):
        SimpleTestWSGIController.tearDown(self)
        warnings.simplefilter('always', DeprecationWarning)

    # def test_legacy_return_etag_cache(self):
    #     warnings.simplefilter('always', DeprecationWarning)
    # 
    #     self.baseenviron['pylons.routes_dict']['action'] = 'legacy_etag_cache'
    #     response = self.app.get('/')
    #     assert 'from etag_cache' in response

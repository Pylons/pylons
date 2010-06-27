import warnings
from unittest import TestCase

from paste.fixture import TestApp
from paste.httpexceptions import HTTPMovedPermanently
from paste.registry import RegistryManager

from __init__ import TestWSGIController


def make_helperscontroller():
    import pylons
    from pylons.controllers import WSGIController
    from pylons.controllers.util import etag_cache
    
    class HelpersController(WSGIController):

        def test_etag_cache(self):
            etag_cache('test')
            return "from etag_cache"
    return HelpersController

class TestHelpers(TestWSGIController):
    def __init__(self, *args, **kargs):
        from pylons.testutil import ControllerWrap, SetupCacheGlobal
        HelpersController = make_helperscontroller()
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(HelpersController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)
        warnings.simplefilter('error', DeprecationWarning)

    def tearDown(self):
        warnings.simplefilter('always', DeprecationWarning)

    def test_return_etag_cache(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'test_etag_cache'
        response = self.app.get('/')
        assert '"test"' == response.header('Etag')
        assert 'from etag_cache' in response

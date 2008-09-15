import warnings
from unittest import TestCase

from paste.fixture import TestApp
from paste.httpexceptions import HTTPMovedPermanently
from paste.registry import RegistryManager

import pylons
from pylons import jsonify, Response
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

class HelpersController(WSGIController):
    def imports(self):
        import pylons.helpers
        self.helpers = pylons.helpers

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

    def test_abort(self):
        try:
            self.wsgi_app.abort()
        except DeprecationWarning, msg:
            assert ('The abort function has moved to pylons.controllers.util, '
                    'please update your import statements to reflect the '
                    'move') in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'

    def test_etag_cache(self):
        try:
            self.wsgi_app.etag_cache()
        except DeprecationWarning, msg:
            assert ('The etag_cache function has moved to '
                    'pylons.controllers.util, please update your import '
                    'statements to reflect the move') in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'

    def test_redirect_to(self):
        try:
            self.wsgi_app.redirect_to()
        except DeprecationWarning, msg:
            assert ('The redirect_to function has moved to '
                    'pylons.controllers.util, please update your import '
                    'statements to reflect the move') in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'


class MiscLegacyController(WSGIController):

    def legacy_httpexception(self):
        raise HTTPMovedPermanently('/elsewhere')

    def legacy_response(self):
        return Response('Legacy Response!')

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

    def test_legacy_httpexception(self):
        self.baseenviron['pylons.routes_dict']['action'] = \
            'legacy_httpexception'
        try:
            self.app.get('/')
        except DeprecationWarning, msg:
            assert ('Raising a paste.httpexceptions.HTTPException is '
                    'deprecated, use webob.exc.HTTPException instead') \
                    in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'

    def test_legacy_httpexception_to_response(self):
        self.baseenviron['pylons.routes_dict']['action'] = \
            'legacy_httpexception'
        warnings.simplefilter('always', DeprecationWarning)
        self.app.get('/', status=301)

    def test_legacy_response_deprecated(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'legacy_response'
        try:
            self.app.get('/')
        except DeprecationWarning, msg:
            assert pylons.legacy.response_warning in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'

    def test_legacy_response(self):
        warnings.simplefilter('always', DeprecationWarning)

        self.baseenviron['pylons.routes_dict']['action'] = 'legacy_response'
        response = self.app.get('/')
        assert 'Legacy Response!' in response

    def test_legacy_etag_cache_deprecated(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'legacy_etag_cache'
        try:
            self.app.get('/')
        except DeprecationWarning, msg:
            assert pylons.legacy.response_warning in msg[0], msg
        else:
            assert False, 'Expected a DeprecationWarning'

    def test_legacy_return_etag_cache(self):
        warnings.simplefilter('always', DeprecationWarning)

        self.baseenviron['pylons.routes_dict']['action'] = 'legacy_etag_cache'
        response = self.app.get('/')
        assert 'from etag_cache' in response

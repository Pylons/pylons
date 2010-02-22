from paste.fixture import TestApp
from paste.registry import RegistryManager

from routes.middleware import RoutesMiddleware

from pylons import request, url
from pylons.decorators.secure import https
from pylons.controllers import WSGIController
from pylons.testutil import ControllerWrap, SetupCacheGlobal

from __init__ import TestWSGIController

class HttpsController(WSGIController):

    @https('/pylons')
    def index(self):
        return 'index page'

    @https(lambda: url(controller='auth', action='login'))
    def login2(self):
        return 'login2 page'

    @https(lambda: request.url)
    def secure(self):
        return 'secure page'

    @https()
    def get(self):
        return 'get page'

class TestHttpsDecorator(TestWSGIController):
    def setUp(self):
        TestWSGIController.setUp(self)
        from routes import Mapper
        map = Mapper()
        map.connect('/:action')
        map.connect('/:action/:id')
        map.connect('/:controller/:action/:id')
        map.connect('/:controller/:action')
        app = ControllerWrap(HttpsController)
        app = SetupCacheGlobal(app, self.environ, setup_cache=False)
        app = RoutesMiddleware(app, map)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_https_explicit_path(self):
        self.environ['pylons.routes_dict']['action'] = 'index'

        response = self.app.get('/index', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/pylons'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/index', status=200)
        assert 'location' not in response.header_dict
        assert 'index page' in response

    def test_https_disallows_post(self):
        self.environ['pylons.routes_dict']['action'] = 'index'
        response = self.app.post('/index', status=405)

    def test_https_callable(self):
        self.environ['pylons.routes_dict']['action'] = 'login2'

        response = self.app.get('/login2', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/auth/login'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/login2', status=200)
        assert 'location' not in response.header_dict
        assert 'login2 page' in response

    def test_https_callable_current(self):
        self.environ['pylons.routes_dict']['action'] = 'secure'

        response = self.app.get('/secure', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/secure'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/secure', status=200)
        assert 'location' not in response.header_dict
        assert 'secure page' in response

    def test_https_redirect_to_self(self):
        self.environ['pylons.routes_dict']['action'] = 'get'

        response = self.app.get('/get', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/get'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/get', status=200)
        assert 'location' not in response.header_dict
        assert 'get page' in response

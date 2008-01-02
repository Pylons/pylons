from paste.fixture import TestApp
from paste.registry import RegistryManager

from routes.middleware import RoutesMiddleware

from pylons.decorators.secure import https

from pylons.controllers import WSGIController
from pylons.testutil import ControllerWrap, SetupCacheGlobal

from __init__ import TestWSGIController

class HttpsController(WSGIController):
    def index(self):
        return 'index page'
    index = https('/pylons')(index)

    def login(self):
        return 'login page'
    login = https(controller='auth', action='login')(login)

    def get(self):
        return 'get page'
    get = https()(get)

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

    def test_https_url_for_kwargs(self):
        self.environ['pylons.routes_dict']['action'] = 'login'

        response = self.app.get('/login', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/auth/login'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/login', status=200)
        assert 'location' not in response.header_dict
        assert 'login page' in response

    def test_https_redirect_to_self(self):
        self.environ['pylons.routes_dict']['action'] = 'get'

        response = self.app.get('/get', status=302)
        assert response.header_dict.get('location') == \
            'https://localhost/get'

        self.environ['wsgi.url_scheme'] = 'https'
        response = self.app.get('/get', status=200)
        assert 'location' not in response.header_dict
        assert 'get page' in response

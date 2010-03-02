import os
import sys

import pylons
from beaker.cache import CacheManager
from beaker.middleware import SessionMiddleware
from paste.fixture import TestApp
from paste.registry import RegistryManager
from paste.deploy.converters import asbool
from pylons.decorators import jsonify
from pylons.configuration import PylonsConfig
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes import Mapper
from routes.middleware import RoutesMiddleware


def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=root, controllers=os.path.join(root, 'sample_controllers', 'controllers'))
    sys.path.append(root)

    config = PylonsConfig()
    config.init_app(global_conf, app_conf, package='sample_controllers', paths=paths)
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.connect('/{controller}/{action}')
    config['routes.map'] = map
    
    class AppGlobals(object): pass
    config['pylons.app_globals'] = AppGlobals()
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    app = SessionMiddleware(app, config)

    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [401, 403, 404, 500])
    app = RegistryManager(app)

    app.config = config
    return app

class TestJsonifyDecorator(object):
    def setUp(self):
        self.app = TestApp(make_app(dict(full_stack=True)))
    
    def test_basic_response(self):
        response = self.app.get('/hello/index')
        assert 'Hello World' in response

import os
import sys

from beaker.middleware import SessionMiddleware
from paste.fixture import TestApp
from paste.registry import RegistryManager
from paste.deploy.converters import asbool
from routes import Mapper
from routes.middleware import RoutesMiddleware

from nose.tools import raises

from __init__ import test_root


def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    import pylons.configuration as configuration
    from pylons.middleware import ErrorHandler, StatusCodeRedirect
    from pylons.wsgiapp import PylonsApp
    
    import event_file
    
    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=os.path.join(test_root, 'sample_controllers'), controllers=os.path.join(test_root, 'sample_controllers', 'controllers'))
    sys.path.append(test_root)

    config = configuration.PylonsConfig()
    config.init_app(global_conf, app_conf, package='sample_controllers', paths=paths)
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.connect('/{controller}/{action}')
    config['routes.map'] = map
    
    class AppGlobals(object): pass
    config['pylons.app_globals'] = AppGlobals()
    
    config.scan(event_file)
    
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

class TestEvents(object):
    def setUp(self):
        self.app = TestApp(make_app({}))
    
    def test_basic_response(self):
        response = self.app.get('/hello/index')
        assert 'Hello World' in response
        
    def test_new_request_event(self):
        response = self.app.get('/hello/index')
        assert hasattr(response.req, 'reg')
        assert response.req.reg == True
    
    def test_new_response_event(self):
        response = self.app.get('/hello/index')
        assert response.response.reg == True

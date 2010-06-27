import os
import re
import sys

from beaker.cache import CacheManager
from beaker.middleware import SessionMiddleware, CacheMiddleware
from mako.lookup import TemplateLookup
from nose.tools import raises
from paste.fixture import TestApp
from paste.registry import RegistryManager
from paste.deploy.converters import asbool
from routes import Mapper
from routes.middleware import RoutesMiddleware

from nose.tools import raises

from __init__ import test_root


def make_app(global_conf, full_stack=True, static_files=True, include_cache_middleware=False, attribsafe=False, **app_conf):
    import pylons
    import pylons.configuration as configuration
    from pylons import url
    from pylons.decorators import jsonify
    from pylons.middleware import ErrorHandler, StatusCodeRedirect
    from pylons.error import handle_mako_error
    from pylons.wsgiapp import PylonsApp

    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=os.path.join(test_root, 'sample_controllers'), controllers=os.path.join(test_root, 'sample_controllers', 'controllers'),
                 templates=os.path.join(test_root, 'sample_controllers', 'templates'))
    sys.path.append(test_root)

    config = configuration.PylonsConfig()
    config.init_app(global_conf, app_conf, package='sample_controllers', paths=paths)
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.connect('/{controller}/{action}')
    config['routes.map'] = map
    
    class AppGlobals(object): pass
    
    config['pylons.app_globals'] = AppGlobals()
    
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'], imports=['from markupsafe import escape']
    )
        
    if attribsafe:
        config['pylons.strict_tmpl_context'] = False
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    if include_cache_middleware:
        app = CacheMiddleware(app, config)
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

class TestTemplatingApp(object):
    def setUp(self):
        self.app = TestApp(make_app({'cache_dir': os.path.join(os.path.dirname(__file__), 'cache')}, include_cache_middleware=True))
    
    def test_testvars(self):
        resp = self.app.get('/hello/intro_template')
        assert 'Hi there 6' in resp
    
    def test_template_cache(self):
        resp = self.app.get('/hello/time_template')
        resp2 = self.app.get('/hello/time_template')
        assert resp.body == resp2.body


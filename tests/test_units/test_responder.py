# -*- coding: utf-8 -*-
import os
import re
import sys

import pylons
import pylons.configuration as configuration
from nose.tools import raises
from paste.fixture import TestApp
from pylons import url
from pylons.controllers.util import abort, Response
from pylons.wsgiapp import PylonsApp
from routes import Mapper
from routes.middleware import RoutesMiddleware
from routes.util import URLGenerator

from nose.tools import raises

config = None

class Smith(object):
    def __init__(self, req):
        self.req = req
    
    def __call__(self):
        return Response('Hello Smith')

class Doe(object):
    def __init__(self, req):
        self.req = req
    
    def index(self):
        return Response('Hello Doe')
    
    def not_here(self):
        abort(404)
    
    not_callable = 42
        

class Fawn(object):
    def __init__(self, req):
        abort(401)

def plain_view(request):
    return Response('Plain View')


def make_app(global_conf, debug=True, **app_conf):
    global config
    config = configuration.PylonsConfig()
    config.begin()
    if debug:
        config['debug'] = True
    config.add_route('/smith', view=Smith)
    config.add_route('/doe', view=Doe, action='index')
    config.add_route('/doe/not_here', view=Doe, action='not_here')
    config.add_route('/doe/not_callable', view=Doe, action='not_callable')
    config.add_route('/fawn', view=Fawn)
    config.add_route('/plainview', view=plain_view)
    config.add_route('/aview', view='sample_controllers.controllers.hello:a_view')
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    app.config = config
    return app

class TestWsgiApp(object):
    def setUp(self):
        self.app = TestApp(make_app({}))
        url._push_object(URLGenerator(config['routes.map'], {}))
    
    def test_class_view(self):
        resp = self.app.get('/smith')
        assert 'Hello Smith' in resp
    
    def test_index_view(self):
        resp = self.app.get('/doe')
        assert 'Hello Doe' in resp
    
    def test_401_class_init(self):
        resp = self.app.get('/fawn', expect_errors=True)
        assert resp.status == 401
    
    def test_plain_view(self):
        resp = self.app.get('/plainview')
        assert 'Plain View' in resp
    
    def test_a_view(self):
        resp = self.app.get('/aview')
        assert 'A View' in resp

    def test_404_class_method(self):
        resp = self.app.get('/doe/not_here', expect_errors=True)
        assert resp.status == 404

    @raises(Exception)
    def test_non_callable(self):
        resp = self.app.get('/doe/not_callable')
    
    @raises(Exception)
    def test_not_callable_view(self):
        not_callable = 42
        config = configuration.PylonsConfig()
        config.begin()
        config.add_route('/smith', view=not_callable)
    
    @raises(Exception)
    def test_no_action(self):
        config = configuration.PylonsConfig()
        config.begin()
        config.add_route('/smith', view=Doe, action='no_action_here')

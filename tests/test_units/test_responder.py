# -*- coding: utf-8 -*-
import os
import re
import sys

import pylons
import pylons.configuration as configuration
from nose.tools import raises
from paste.fixture import TestApp
from pylons import url
from pylons.controllers import RouteResponder
from pylons.controllers.util import abort, Response
from pylons.wsgiapp import PylonsApp
from routes import Mapper
from routes.middleware import RoutesMiddleware
from routes.util import URLGenerator

from nose.tools import raises

config = None

class Smith(RouteResponder):
    def index(self):
        return Response('Hello World')

class Doe(RouteResponder):
    def _before(self):
        self.msg = 'Hello World'
    
    def index(self):
        return Response(self.msg)
    
    def not_here(self):
        abort(401)
    
    def _after(self):
        self._request.after_msg = 'Hi there'

class Epsy(RouteResponder):
    def _before(self):
        abort(404)
    
    def index(self):
        return Response('Never get here....')


def make_app(global_conf, debug=True, **app_conf):
    global config
    config = configuration.PylonsConfig()
    config.begin()
    if debug:
        config['debug'] = True
    config.add_route('/smith/{action}', responder=Smith)
    config.add_route('/doe/{action}', responder=Doe)
    config.add_route('/epsy/{action}', responder=Epsy)
    config.add_route('/jones', responder=Smith)
    
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    app.config = config
    return app

class TestWsgiApp(object):
    def setUp(self):
        self.app = TestApp(make_app({}))
        url._push_object(URLGenerator(config['routes.map'], {}))
    
    def test_helloworld(self):
        resp = self.app.get('/smith/index')
        assert 'Hello World' in resp
    
    @raises(Exception)
    def test_noaction(self):
        resp = self.app.get('/smith/freddy')
    
    @raises(Exception)
    def test_no_route_action(self):
        resp = self.app.get('/jones')

    def test_invalid_action(self):
        resp = self.app.get('/smith/_private', expect_errors=True)
        assert resp.status == 404

    @raises(NotImplementedError)
    def test_unicode_action(self):
        resp = self.app.get('/smith/ОбсуждениеКомпаний', expect_errors=True)

    def test_unicode_404(self):
        app = TestApp(make_app({}, debug=False))
        resp = app.get('/smith/ОбсуждениеКомпаний', expect_errors=True)
        assert resp.status == 404

    def test_before_after(self):
        resp = self.app.get('/doe/index')
        assert 'Hello World' in resp
        assert resp.req.after_msg == 'Hi there'

    def test_before_exception(self):
        resp = self.app.get('/epsy/index', expect_errors=True)
        assert resp.status == 404

    def test_action_exception(self):
        resp = self.app.get('/doe/not_here', expect_errors=True)
        assert resp.status == 401

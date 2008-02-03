# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager
import paste.httpexceptions as httpexceptions

import pylons
from pylons.controllers import ObjectDispatchController
from pylons.decorators import expose

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

class SubController(object):

    def foo(self):
        return 'sub_foo'
    foo = expose()(foo)

    def index(self):
        return 'sub index'
    index = expose()(index)

    def default(self, *args):
        return ("recieved the following args (from the url): %s" % list(args))
    default = expose()(default)


class BasicDispatchController(ObjectDispatchController):

    def index(self):
        return 'hello world'
    index = expose()(index)

    def yield_fun(self):
        def its():
            x = 0
            while x < 100:
                yield 'hi'
                x += 1
        return its()

    def strme(self):
        return "hi there"

    def use_redirect(self):
        pylons.response.set_cookie('message', 'Hello World')
        exc = httpexceptions.get_exception(301)
        raise exc('/elsewhere')

    def header_check(self):
        pylons.response.headers['Content-Type'] = 'text/plain'
        return "Hello all!"

    def nothing(self):
        return

    def default(self, remainder):
        return "Main Default Page called for url /%s" % remainder
    default = expose()(default)

    sub = SubController()

class TestTGController(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(BasicDispatchController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)

    def test_tg_style_default(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'route'
        self.baseenviron['pylons.routes_dict']['url'] = 'sdfaswdfsdfa'
        # random string should be caught by the default route
        resp = self.app.get('/sdfaswdfsdfa')
        print resp
        assert 'Default' in resp.body

    def test_tg_style_index(self):
        # Do TG dispatch
        self.baseenviron['pylons.routes_dict']['action'] = 'route'
        self.baseenviron['pylons.routes_dict']['url'] = 'index'
        resp = self.app.get('/index/')
        assert 'hello' in resp.body

    def test_tg_style_subcontroller_index(self):
        # Do TG dispatch
        self.baseenviron['pylons.routes_dict']['action'] = 'route'
        self.baseenviron['pylons.routes_dict']['url'] = 'sub/index'
        resp = self.app.get('/sub/index')
        assert "sub index" in resp.body

    def test_tg_style_subcontroller_default(self):
        # Do TG dispatch
        self.baseenviron['pylons.routes_dict']['action'] = 'route'
        self.baseenviron['pylons.routes_dict']['url'] = 'sub/bob/tim/joe'
        resp = self.app.get('/sub/bob/tim/joe')
        assert "bob" in resp.body
        assert 'tim' in resp.body
        assert 'joe' in resp.body

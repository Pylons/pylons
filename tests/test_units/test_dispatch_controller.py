# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager
import paste.httpexceptions as httpexceptions
import pylons

from pylons.controllers import ObjectDispatchController
from pylons.decorators import expose
from pylons.controllers.util import redirect_to
from routes import Mapper
from routes.middleware import RoutesMiddleware

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap


class SubController(object):
    @expose()
    def foo(self):
        return 'sub_foo'
    
    @expose()
    def index(self):
        return 'sub index'
    
    @expose()
    def default(self, *args):
        return ("recieved the following args (from the url): %s" %list(args))


class BasicDispatchController(ObjectDispatchController):    
    @expose()
    def index(self):
        return 'hello world'

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
    
    @expose()    
    def default(self, remainder):
        return "Main Default Page called for url /%s"%remainder    
        
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
        self.baseenviron['pylons.routes_dict']['url']= 'sdfaswdfsdfa' #Do TG dispatch
        resp = self.app.get('/sdfaswdfsdfa') #random string should be caught by the default route
        assert 'Default' in resp.body
    
    def test_tg_style_index(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'route' #Do TG dispatch
        self.baseenviron['pylons.routes_dict']['url']= 'index'
        resp = self.app.get('/index/')
        assert 'hello' in resp.body
        
    def test_tg_style_subcontroller_index(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'route' #Do TG dispatch
        self.baseenviron['pylons.routes_dict']['url']= 'sub/index'
        resp = self.app.get('/sub/index')
        assert "sub index" in resp.body
    
    def test_tg_style_subcontroller_default(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'route' #Do TG dispatch
        self.baseenviron['pylons.routes_dict']['url']= 'sub/bob/tim/joe'
        resp=self.app.get('/sub/bob/tim/joe')
        assert "bob" in resp.body
        assert 'tim' in resp.body
        assert 'joe' in resp.body 

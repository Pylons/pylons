# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager
from webob.exc import status_map

import pylons
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect_to

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap, TestMiddleware

class BasicWSGIController(WSGIController):
    def __before__(self):
        pylons.response.headers['Cache-Control'] = 'private'
    
    def __after__(self):
        pylons.response.set_cookie('big_message', 'goodbye')
    
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
        exc = status_map[301]
        raise exc('/elsewhere').exception
    
    def use_customnotfound(self):
        exc = status_map[404]
        raise exc('Custom not found').exception
    
    def header_check(self):
        pylons.response.headers['Content-Type'] = 'text/plain'
        return "Hello all!"
    
    def nothing(self):
        return

    def params(self):
        items = pylons.request.params.mixed().items()
        items.sort()
        return str(items)

    def list(self):
        return ['from', ' a ', 'list']

class FilteredWSGIController(WSGIController):
    def __init__(self):
        self.before = 0
        self.after = 0

    def __before__(self):
        self.before += 1

    def __after__(self):
        self.after += 1
        action = pylons.request.environ['pylons.routes_dict'].get('action')
        if action in ('after_response', 'after_string_response'):
            pylons.response.write(' from __after__')

    def index(self):
        return 'hi all, before is %s' % self.before

    def after_response(self):
        return 'hi'

    def after_string_response(self):
        return 'hello'

class TestBasicWSGI(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(BasicWSGIController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = TestMiddleware(app)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)

    def test_wsgi_call(self):
        resp = self.get_response()
        assert 'hello world' in resp
    
    def test_yield_wrapper(self):
        resp = self.get_response(action='yield_fun')
        assert 'hi' * 100 in resp

    def test_404(self):
        self.environ['paste.config']['global_conf']['debug'] = False
        self.environ['pylons.routes_dict']['action'] = 'notthere'
        resp = self.app.get('/', status=404)
        assert resp.status == 404
    
    def test_404exception(self):
        self.environ['paste.config']['global_conf']['debug'] = False
        self.environ['pylons.routes_dict']['action'] = 'use_customnotfound'
        resp = self.app.get('/', status=404)
        assert 'pylons.controller.exception' in resp.environ
        exc = resp.environ['pylons.controller.exception']
        assert exc.detail == 'Custom not found'
        assert resp.status == 404
    
    def test_private_func(self):
        self.baseenviron['pylons.routes_dict']['action'] = '_private'
        resp = self.app.get('/', status=404)
        assert resp.status == 404
    
    def test_strme_func(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'strme'
        resp = self.app.get('/')
        assert "hi there" in resp
    
    def test_header_check(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'header_check'
        resp = self.app.get('/')
        assert "Hello all!" in resp
        assert resp.response.headers['Content-Type'] == 'text/plain'
        assert resp.response.headers['Cache-Control'] == 'private'
        assert resp.header('Content-Type') == 'text/plain'
    
    def test_head(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'header_check'
        resp = self.app._gen_request('HEAD', '/')
        assert '' == resp.body
        assert resp.header('Content-Type') == 'text/plain'

    def test_redirect(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'use_redirect'
        resp = self.app.get('/', status=301)

    def test_nothing(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'nothing'
        resp = self.app.get('/')
        assert '' == resp.body
        assert resp.response.headers['Cache-Control'] == 'private'

    def test_unicode_action(self):
        self.baseenviron['pylons.routes_dict']['action'] = u'ОбсуждениеКомпаний'
        resp = self.app.get('/', status=404)

    def test_params(self):
        self.baseenviron['pylons.routes_dict']['action'] = u'params'
        resp = self.app.get('/?foo=bar')
        assert "[('foo', u'bar')]" in resp, str(resp)
        resp = self.app.post('/?foo=bar', params=dict(snafu='snafoo'))
        assert "[('foo', u'bar'), ('snafu', u'snafoo')]" in resp, str(resp)
        resp = self.app.put('/?foo=bar', params=dict(snafu='snafoo'))
        assert "[('foo', u'bar'), ('snafu', u'snafoo')]" in resp, str(resp)

    def test_list(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'list'
        assert 'from a list' in self.app.get('/')

class TestFilteredWSGI(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(FilteredWSGIController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)
    
    def test_before(self):
        resp = self.get_response(action='index')
        assert 'hi' in resp
        assert 'before is 1' in resp

    def test_after_response(self):
        resp = self.get_response(action='after_response')
        assert 'hi from __after__' in resp

    def test_after_string_response(self):
        resp = self.get_response(action='after_string_response')
        assert 'hello from __after__' in resp

    def test_start_response(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'start_response'
        self.app.get('/', status=404)

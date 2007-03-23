from unittest import TestCase

from paste.wsgiwrappers import WSGIRequest
from paste.fixture import TestApp
from paste.registry import RegistryManager

import pylons
from pylons.util import ContextObj
from pylons.controllers import Controller, WSGIController, XMLRPCController

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

class BasicController(Controller):
    def index(self):
        return "hi all"

    def view(self, id, name):
        return "Hi %s, %s" % (id, name)
    
    def kargs(self, id, **kargs):
        return [id, kargs]

class BasicFilteredController(Controller):
    def __init__(self):
        self.before = 0
        self.after = 0

    def __before__(self):
        self.before += 1

    def __after__(self):
        self.after += 1

    def index(self):
        return 'hi all, before is %s' % self.before

class BasicWSGIController(WSGIController):
    def index(self):
        return pylons.Response('hello world')

    def yield_fun(self):
        def its():
            x = 0
            while x < 100:
                yield 'hi'
                x += 1
        return its()
    
    def strme(self):
        return "hi there"

class FilteredWSGIController(WSGIController):
    def __init__(self):
        self.before = 0
        self.after = 0

    def __before__(self):
        self.before += 1

    def __after__(self):
        self.after += 1

    def index(self):
        return pylons.Response('hi all, before is %s' % self.before)


class TestBasicController(TestCase):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True))}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = BasicController()
        self.controller.start_response = None
    
    def tearDown(self):
        pylons.request._pop_object()
        pylons.c._pop_object()

    def test_basic_call(self):
        assert "hi all" == self.controller()
    
    def test_inspect_call(self):
        self.environ['pylons.routes_dict'].update(dict(action='view', id=4, name='fred'))
        assert "Hi 4, fred" == self.controller()

    def test_private_action(self):
        self.environ['pylons.routes_dict']['action'] = '_private'
        response = self.controller()
        assert isinstance(response, pylons.Response)
        assert response.status_code == 404
    
    def test_attach_locals(self):
        pylons.g._push_object(object())
        pylons.session._push_object(object())
        pylons.cache._push_object(object())
        pylons.buffet._push_object(object())
        c = id(pylons.c._current_obj())
        g = id(pylons.g._current_obj())
        cache = id(pylons.cache._current_obj())
        session = id(pylons.session._current_obj())
        request = id(pylons.request._current_obj())
        buffet = id(pylons.buffet._current_obj())
        cr = self.controller
        cr._attach_locals()
        assert c == id(cr.c)
        assert g == id(cr.g)
        assert request == id(cr.request)
        assert cache == id(cr.cache)
        assert session == id(cr.session)
        assert buffet == id(cr.buffet)
    
    def test_kwargs_call(self):
        self.environ['pylons.routes_dict'].update(dict(action='kargs', id=4, 
                                                       name='fred'))
        id, kargs = self.controller()
        assert id == 4
        assert kargs == {'action': 'kargs', 'start_response': None, 
                         'environ': self.environ, 'name': 'fred'}

    def test_method_missing(self):
        self.environ['pylons.routes_dict']['action'] = 'notthere'
        self.assertRaises(NotImplementedError, self.controller)
        
class TestFilteredController(TestCase):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True))}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = BasicFilteredController()
        self.controller.start_response = None
    
    def tearDown(self):
        pylons.request._pop_object()
        pylons.c._pop_object()

    def test_basic_call(self):
        resp = self.controller()
        assert "hi all" in resp
        assert "before is 1" in resp

class TestBasicWSGI(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(BasicWSGIController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron, setup_cache=False)
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
    
    def test_private_func(self):
        self.baseenviron['pylons.routes_dict']['action'] = '_private'
        resp = self.app.get('/', status=404)
        assert resp.status == 404
    
    def test_strme_func(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'strme'
        resp = self.app.get('/')
        assert "hi there" in resp


class TestFilteredWSGI(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(FilteredWSGIController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron, setup_cache=False)
        app = RegistryManager(app)
        self.app = TestApp(app)
        
    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)
    
    def test_before(self):
        resp = self.get_response(action='index')
        assert 'hi' in resp
        assert 'before is 1' in resp

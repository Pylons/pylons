from paste.wsgiwrappers import WSGIRequest
from paste.fixture import TestApp

import pylons
from pylons.util import ContextObj
from pylons.controllers import Controller, WSGIController, XMLRPCController

class SampleController(Controller):
    def index(self):
        return "hi all"

    def view(self, id, name):
        return "Hi %s, %s" % (id, name)
    
    def kargs(self, id, **kargs):
        return [id, kargs]

class SampleWSGIController(WSGIController):
    def index(self):
        return pylons.Response('hello world')

class TestController(object):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index')}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = SampleController()
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
        

class TestWSGIController(object):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index')}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = SampleWSGIController()
        self.controller.start_response = None
        self.app = TestApp(self.controller)

    def test_wsgi_call(self):
        resp = self.app.get('/', extra_environ=self.environ)
        assert 'hello world' in resp

from paste.wsgiwrappers import WSGIRequest

import pylons
from pylons.util import ContextObj
from pylons.controllers import Controller, WSGIController, XMLRPCController

class SampleController(Controller):
    def index(self):
        return "hi all"

class TestController(object):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index')}
        pylons.request._push_object(WSGIRequest(self.environ))
        pylons.c._push_object(ContextObj())
        self.controller = SampleController()
        self.controller.start_response = None

    def test_basic_call(self):
        assert "hi all" == self.controller()
    
    def test_private_action(self):
        self.environ['pylons.routes_dict']['action'] = '_private'
        response = self.controller()
        assert isinstance(response, pylons.Response)
        assert response.status_code == 404

import os
from unittest import TestCase
from xmlrpclib import loads, dumps

import pylons
from pylons.util import ContextObj, PylonsContext
from pylons.testutil import ControllerWrap, SetupCacheGlobal
from routes import request_config

data_dir = os.path.dirname(os.path.abspath(__file__))

try:
    shutil.rmtree(data_dir)
except:
    pass

class TestWSGIController(TestCase):
    def setUp(self):
        c = ContextObj()
        py_obj = PylonsContext()
        py_obj.c = c
        py_obj.request = py_obj.response = None
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True)),
                        'pylons.pylons':py_obj}
        pylons.c._push_object(c)

    def tearDown(self):
        pylons.c._pop_object()
    
    def get_response(self, **kargs):
        test_args = kargs.pop('test_args', {})
        url = kargs.pop('_url', '/')
        self.environ['pylons.routes_dict'].update(kargs)
        return self.app.get(url, extra_environ=self.environ, **test_args)

    def post_response(self, **kargs):
        url = kargs.pop('_url', '/')
        self.environ['pylons.routes_dict'].update(kargs)
        return self.app.post(url, extra_environ=self.environ, params=kargs)
    
    def xmlreq(self, method, args=None):
        if args is None:
            args = ()
        ee = dict(CONTENT_TYPE='text/xml')
        data = dumps(args, methodname=method)
        self.response = response = self.app.post('/', params = data, extra_environ=ee)
        return loads(response.body)[0][0]
    


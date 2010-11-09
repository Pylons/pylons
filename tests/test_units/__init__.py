import json
import os
import sys
from unittest import TestCase
from urllib import quote_plus
from xmlrpclib import loads, dumps
    
data_dir = os.path.dirname(os.path.abspath(__file__))

try:
    shutil.rmtree(data_dir)
except:
    pass

cur_dir = os.path.dirname(os.path.abspath(__file__))
pylons_root = os.path.dirname(os.path.dirname(cur_dir))
test_root = os.path.join(pylons_root, 'test_files')

sys.path.append(test_root)

class TestMiddleware(object):
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        if 'paste.testing_variables' not in environ:
            environ['paste.testing_variables'] = {}
        testenv = environ['paste.testing_variables']
        testenv['environ'] = environ
        return self.app(environ, start_response)


class TestWSGIController(TestCase):
    def setUp(self):
        import pylons
        from pylons.util import ContextObj, PylonsContext
        
        c = ContextObj()
        py_obj = PylonsContext()
        py_obj.tmpl_context = c
        py_obj.request = py_obj.response = None
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True)),
                        'pylons.pylons':py_obj}
        pylons.tmpl_context._push_object(c)

    def tearDown(self):
        import pylons
        pylons.tmpl_context._pop_object()
    
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
        self.response = response = self.app.post('/', params = data,
                                                 extra_environ=ee)
        return loads(response.body)[0][0]

    def jsonreq(self, method, args=()):
        assert(isinstance(args, list) or
               isinstance(args, tuple) or
               isinstance(args, dict))

        ee = dict(CONTENT_TYPE='application/json')
        data = json.dumps(dict(id='test',
                               method=method,
                               params=args))
        self.response = response = self.app.post('/', params=quote_plus(data),
                                                 extra_environ=ee)
        return json.loads(response.body)
        

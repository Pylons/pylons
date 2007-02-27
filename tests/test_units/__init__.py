from unittest import TestCase
from xmlrpclib import loads, dumps

from paste.wsgiwrappers import WSGIRequest

import pylons
from pylons.util import ContextObj

class TestWSGIController(TestCase):
    def setUp(self):
        self.environ = {'pylons.routes_dict':dict(action='index'),
                        'paste.config':dict(global_conf=dict(debug=True))}
        pylons.c._push_object(ContextObj())

    def tearDown(self):
        pylons.c._pop_object()
    
    def get_response(self, **kargs):
        url = kargs.pop('_url', '/')
        self.environ['pylons.routes_dict'].update(kargs)
        return self.app.get(url)
    
    def xmlreq(self, method, args=None):
        if args is None:
            args = ()
        ee = dict(CONTENT_TYPE='text/xml')
        data = dumps(args, methodname=method)
        response = self.app.post('/', params = data, extra_environ=ee)
        return loads(response.body)[0][0]
    

class ControllerWrap(object):
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, environ, start_response):
        app = self.controller()
        app.start_response = None
        return app(environ, start_response)

class SetupCacheGlobal(object):
    def __init__(self, app, environ, setup_g=True, setup_cache=True):
        if setup_g:
            g = type('G object', (object,), {})
            g.message = 'Hello'
            g.counter = 0
            g.pylons_config = type('App conf', (object,), {})
            g.pylons_config.app_conf = dict(cache_enabled='True')
            self.g = g
        self.app = app
        self.environ = environ
        self.setup_cache = setup_cache
        self.setup_g = setup_g

    def __call__(self, environ, start_response):
        registry = environ['paste.registry']
        if self.setup_cache:
            registry.register(pylons.cache, environ['beaker.cache'])
        if self.setup_g:
            registry.register(pylons.g, self.g)

        # Update the environ
        environ.update(self.environ)
        registry.register(pylons.request, WSGIRequest(environ))
        return self.app(environ, start_response)

import os
import shutil
import time

from paste.fixture import TestApp
from paste.registry import RegistryManager

from beaker.middleware import CacheMiddleware

import pylons
from pylons.decorators.cache import beaker_cache, create_cache_key

from pylons.controllers import WSGIController, XMLRPCController
from pylons.testutil import SetupCacheGlobal, ControllerWrap

from __init__ import data_dir, TestWSGIController

class CacheController(WSGIController):
    def test_default_cache_decorator(self):
        pylons.g.counter += 1
        return 'Counter=%s' % pylons.g.counter
    test_default_cache_decorator = beaker_cache(key=None)(test_default_cache_decorator)
    
    def test_get_cache_decorator(self):
        pylons.g.counter += 1
        return 'Counter=%s' % pylons.g.counter
    test_get_cache_decorator = beaker_cache(key="param", query_args=True)(test_get_cache_decorator)

    def test_get_cache_default(self):
        pylons.g.counter += 1
        return 'Counter=%s' % pylons.g.counter
    test_get_cache_default = beaker_cache(query_args=True)(test_get_cache_default)
    
    def test_expire_cache_decorator(self):
        pylons.g.counter += 1
        return 'Counter=%s' % pylons.g.counter
    test_expire_cache_decorator = beaker_cache(expire=1)(test_expire_cache_decorator)
    
    def test_key_cache_decorator(self, id):
        pylons.g.counter += 1
        return 'Counter=%s, id=%s' % (pylons.g.counter, id)
    test_key_cache_decorator = beaker_cache(key="id")(test_key_cache_decorator)
    
    def test_keyslist_cache_decorator(self, id, id2="123"):
        pylons.g.counter += 1
        return 'Counter=%s, id=%s' % (pylons.g.counter, id)
    test_keyslist_cache_decorator = beaker_cache(key=["id", "id2"])(test_keyslist_cache_decorator)

    def test_invalidate_cache(self):
        ns, key = create_cache_key(CacheController.test_default_cache_decorator)
        c = pylons.cache.get_cache(ns)
        c.remove_value(key)
    
    def test_header_cache(self):
        pylons.response.headers['Content-Type'] = 'application/special'
        pylons.response.headers['x-powered-by'] = 'pylons'
        pylons.response.headers['x-dont-include'] = 'should not be included'
        return "Hello folks, time is %s" % time.time()
    test_header_cache = beaker_cache(cache_headers=('content-type','content-length', 'x-powered-by'))(test_header_cache)

cache_dir = os.path.join(data_dir, 'cache')

try:
    shutil.rmtree(cache_dir)
except:
    pass

environ = {}
app = ControllerWrap(CacheController)
app = sap = SetupCacheGlobal(app, environ, setup_cache=True)
app = CacheMiddleware(app, {}, data_dir=cache_dir)
app = RegistryManager(app)
app = TestApp(app)

class TestCacheDecorator(TestWSGIController):
    def setUp(self):
        self.app = app
        TestWSGIController.setUp(self)
        environ.update(self.environ)
        
    def test_default_cache_decorator(self):
        sap.g.counter = 0
        self.get_response(action='test_invalidate_cache')

        response = self.get_response(action='test_default_cache_decorator')
        assert 'text/html' in response.header_dict['content-type']
        assert 'Counter=1' in response

        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        
        response = self.get_response(action='test_get_cache_decorator', _url='/?param=123')
        assert 'Counter=2' in response
        response = self.get_response(action='test_get_cache_decorator', _url="/?param=123")
        assert 'Counter=2' in response
        
        response = self.get_response(action='test_expire_cache_decorator')
        assert 'Counter=3' in response
        response = self.get_response(action='test_expire_cache_decorator')
        assert 'Counter=3' in response
        time.sleep(1)
        response = self.get_response(action='test_expire_cache_decorator')
        assert 'Counter=4' in response
        
        response = self.get_response(action='test_key_cache_decorator', id=1)
        assert 'Counter=5' in response
        response = self.get_response(action='test_key_cache_decorator', id=2)
        assert 'Counter=6' in response
        response = self.get_response(action='test_key_cache_decorator', id=1)
        assert 'Counter=5' in response
        
        response = self.get_response(action='test_keyslist_cache_decorator', id=1, id2=2)
        assert 'Counter=7' in response
        response = self.get_response(action='test_keyslist_cache_decorator', id=1, id2=2)
        assert 'Counter=7' in response
        
        response = self.get_response(action='test_get_cache_default', _url='/?param=1243')
        assert 'Counter=8' in response
        response = self.get_response(action='test_get_cache_default', _url="/?param=123")
        assert 'Counter=2' in response
        response = self.get_response(action='test_get_cache_default', _url="/?param=1243")
        assert 'Counter=8' in response
    
    def test_cache_key(self):
        key = create_cache_key(TestCacheDecorator.test_default_cache_decorator)
        assert key == ('%s.TestCacheDecorator' % self.__module__, 'test_default_cache_decorator')
        
        response = self.get_response(action='test_invalidate_cache')
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        response = self.get_response(action='test_invalidate_cache')
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=2' in response
        
        
    def test_header_cache(self):
        response = self.get_response(action='test_header_cache')
        assert response.header_dict['content-type'] == 'application/special'
        assert response.header_dict['x-powered-by'] == 'pylons'
        assert 'x-dont-include' not in response.header_dict
        output = response.body

        time.sleep(1)
        response = self.get_response(action='test_header_cache')
        assert response.body == output
        assert response.header_dict['content-type'] == 'application/special'
        assert response.header_dict['x-powered-by'] == 'pylons'
        assert 'x-dont-include' not in response.header_dict
        
    def test_nocache(self):
        sap.g.counter = 0
        pylons.config['cache_enabled'] = 'False'
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=2' in response
        pylons.config['cache_enabled'] = 'True'

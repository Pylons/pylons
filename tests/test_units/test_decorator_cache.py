import os
import shutil
import time

from webtest import TestApp
from paste.registry import RegistryManager

from beaker.middleware import CacheMiddleware

import pylons
from pylons.decorators.cache import beaker_cache, create_cache_key

from pylons.controllers import WSGIController, XMLRPCController
from pylons.testutil import SetupCacheGlobal, ControllerWrap

from __init__ import data_dir, TestWSGIController

class CacheController(WSGIController):

    @beaker_cache(key=None)
    def test_default_cache_decorator(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    def test_default_cache_decorator_func(self):
        def func():
            pylons.app_globals.counter += 1
            return 'Counter=%s' % pylons.app_globals.counter
        func = beaker_cache(key=None)(func)
        return func()
    
    def test_response_cache_func(self, use_cache_status=True):
        pylons.response.status_int = 404
        def func():
            pylons.app_globals.counter += 1
            return 'Counter=%s' % pylons.app_globals.counter
        if use_cache_status:
            func = beaker_cache(key=None)(func)
        else:
            func = beaker_cache(key=None, cache_response=False)(func)
        return func()

    @beaker_cache(key=None, type='dbm')
    def test_dbm_cache_decorator(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    @beaker_cache(key="param", query_args=True)
    def test_get_cache_decorator(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    @beaker_cache(query_args=True)
    def test_get_cache_default(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    @beaker_cache(expire=1)
    def test_expire_cache_decorator(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    @beaker_cache(expire=1)
    def test_expire_dbm_cache_decorator(self):
        pylons.app_globals.counter += 1
        return 'Counter=%s' % pylons.app_globals.counter

    @beaker_cache(key="id")
    def test_key_cache_decorator(self, id):
        pylons.app_globals.counter += 1
        return 'Counter=%s, id=%s' % (pylons.app_globals.counter, id)

    @beaker_cache(key=["id", "id2"])
    def test_keyslist_cache_decorator(self, id, id2="123"):
        pylons.app_globals.counter += 1
        return 'Counter=%s, id=%s' % (pylons.app_globals.counter, id)

    def test_invalidate_cache(self):
        ns, key = create_cache_key(CacheController.test_default_cache_decorator)
        c = pylons.cache.get_cache(ns)
        c.remove_value(key)

    def test_invalidate_dbm_cache(self):
        ns, key = create_cache_key(CacheController.test_dbm_cache_decorator)
        c = pylons.cache.get_cache(ns, type='dbm')
        c.remove_value(key)

    @beaker_cache(cache_headers=('content-type','content-length', 'x-powered-by'))
    def test_header_cache(self):
        pylons.response.headers['Content-Type'] = 'application/special'
        pylons.response.headers['x-powered-by'] = 'pylons'
        pylons.response.headers['x-dont-include'] = 'should not be included'
        return "Hello folks, time is %s" % time.time()

    @beaker_cache(query_args=True)
    def test_cache_key_dupe(self):
        return "Hello folks, time is %s" % time.time()

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
        assert 'text/html' in response.headers['content-type']
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
        response = self.get_response(action='test_get_cache_default', _url="/?param=1243")
        assert 'Counter=8' in response
        response = self.get_response(action='test_get_cache_default', _url="/?param=123")
        assert 'Counter=9' in response

        response = self.get_response(action='test_default_cache_decorator_func')
        assert 'text/html' in response.headers['content-type']
        assert 'Counter=10' in response
        response = self.get_response(action='test_default_cache_decorator_func')
        assert 'Counter=10' in response
        
        response = self.get_response(action='test_response_cache_func', use_cache_status=True)
        
        assert 'Counter=10' in response
        
        response = self.get_response(action='test_response_cache_func', use_cache_status=False,
                                     test_args=dict(status=404))
        assert 'Counter=10' in response
        
    
    def test_dbm_cache_decorator(self):
        sap.g.counter = 0
        self.get_response(action="test_invalidate_dbm_cache")
        
        response = self.get_response(action="test_dbm_cache_decorator")
        assert "Counter=1" in response

        response = self.get_response(action="test_dbm_cache_decorator")
        assert "Counter=1" in response
        
        self.get_response(action="test_invalidate_dbm_cache")
        response = self.get_response(action="test_dbm_cache_decorator")
        assert "Counter=2" in response

        sap.g.counter = 0
        response = self.get_response(action="test_expire_dbm_cache_decorator")
        assert "Counter=1" in response
        response = self.get_response(action="test_expire_dbm_cache_decorator")
        assert "Counter=1" in response
        time.sleep(1)
        response = self.get_response(action="test_expire_dbm_cache_decorator")
        assert "Counter=2" in response
        
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

    def test_cache_key_dupe(self):
        response = self.get_response(action='test_cache_key_dupe',
                                     _url='/test_cache_key_dupe?id=1')
        time.sleep(0.1)
        response2 = self.get_response(action='test_cache_key_dupe',
                                      _url='/test_cache_key_dupe?id=2&id=1')
        assert str(response) != str(response2)
        
    def test_header_cache(self):
        response = self.get_response(action='test_header_cache')
        assert response.headers['content-type'] == 'application/special'
        assert response.headers['x-powered-by'] == 'pylons'
        assert 'x-dont-include' not in response.headers
        output = response.body

        time.sleep(1)
        response = self.get_response(action='test_header_cache')
        assert response.body == output
        assert response.headers['content-type'] == 'application/special'
        assert response.headers['x-powered-by'] == 'pylons'
        assert 'x-dont-include' not in response.headers
        
    def test_nocache(self):
        sap.g.counter = 0
        pylons.config['cache_enabled'] = 'False'
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=2' in response
        pylons.config['cache_enabled'] = 'True'

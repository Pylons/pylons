import os
import shutil
import time

from paste.fixture import TestApp
from paste.registry import RegistryManager

from beaker.cache import CacheMiddleware

import pylons
from pylons import Response
from pylons.decorators.cache import beaker_cache

from pylons.controllers import Controller, WSGIController, XMLRPCController

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

class CacheController(WSGIController):
    def test_default_cache_decorator(self):
        pylons.g.counter += 1
        return Response('Counter=%s' % pylons.g.counter)
    test_default_cache_decorator = beaker_cache(key=None)(test_default_cache_decorator)
    
    def test_get_cache_decorator(self):
        pylons.g.counter += 1
        return Response('Counter=%s' % pylons.g.counter)
    test_get_cache_decorator = beaker_cache(key="param", query_args=True)(test_get_cache_decorator)

    def test_get_cache_default(self):
        pylons.g.counter += 1
        return Response('Counter=%s' % pylons.g.counter)
    test_get_cache_default = beaker_cache(query_args=True)(test_get_cache_default)
    
    def test_expire_cache_decorator(self):
        pylons.g.counter += 1
        return Response('Counter=%s' % pylons.g.counter)
    test_expire_cache_decorator = beaker_cache(expire=8)(test_expire_cache_decorator)
    
    def test_key_cache_decorator(self, id):
        pylons.g.counter += 1
        return Response('Counter=%s, id=%s' % (pylons.g.counter, id))
    test_key_cache_decorator = beaker_cache(key="id")(test_key_cache_decorator)
    
    def test_keyslist_cache_decorator(self, id, id2="123"):
        pylons.g.counter += 1
        return Response('Counter=%s, id=%s' % (pylons.g.counter, id))
    test_keyslist_cache_decorator = beaker_cache(key=["id", "id2"])(test_keyslist_cache_decorator)

cachedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')

try:
    shutil.rmtree(cachedir)
except:
    pass

environ = {}
app = ControllerWrap(CacheController)
app = sap = SetupCacheGlobal(app, environ)
app = CacheMiddleware(app, {}, 
    cache_data_dir=cachedir)
app = RegistryManager(app)
app = TestApp(app)

class TestCacheDecorator(TestWSGIController):
    def setUp(self):
        self.app = app
        TestWSGIController.setUp(self)
        environ.update(self.environ)

    def test_default_cache_decorator(self):
        response = self.get_response(action='test_default_cache_decorator')
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
        time.sleep(8)
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
        assert 'Counter=9' in response
        response = self.get_response(action='test_get_cache_default', _url="/?param=1243")
        assert 'Counter=8' in response
        

    def test_nocache(self):
        sap.g.counter = 0
        sap.g.pylons_config.app_conf['cache_enabled'] = 'False'
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=1' in response
        response = self.get_response(action='test_default_cache_decorator')
        assert 'Counter=2' in response
        sap.g.pylons_config.app_conf['cache_enabled'] = 'True'
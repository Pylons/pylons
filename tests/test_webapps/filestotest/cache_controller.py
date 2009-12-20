from pylons import app_globals
from pylons.decorators.cache import beaker_cache
from projectname.lib.base import BaseController

class CacheController(BaseController):

    def test_default_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter
    test_default_cache_decorator = beaker_cache(key=None)(test_default_cache_decorator)
    
    def test_get_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter
    test_get_cache_decorator = beaker_cache(key="param", query_args=True)(test_get_cache_decorator)
    
    def test_expire_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter
    test_expire_cache_decorator = beaker_cache(expire=4)(test_expire_cache_decorator)
    
    def test_key_cache_decorator(self, id):
        app_globals.counter += 1
        return 'Counter=%s, id=%s' % (app_globals.counter, id)
    test_key_cache_decorator = beaker_cache(key="id")(test_key_cache_decorator)
    
    def test_keyslist_cache_decorator(self, id, id2="123"):
        app_globals.counter += 1
        return 'Counter=%s, id=%s' % (app_globals.counter, id)
    test_keyslist_cache_decorator = beaker_cache(key=["id", "id2"])(test_keyslist_cache_decorator)

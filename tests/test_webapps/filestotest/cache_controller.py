from pylons import app_globals as g
from pylons.decorators.cache import beaker_cache
from pylons.templating import render_response
from projectname.lib.base import BaseController

class CacheController(BaseController):

    def test_default_cache_decorator(self):
        g.counter += 1
        return 'Counter=%s' % g.counter
    test_default_cache_decorator = beaker_cache(key=None)(test_default_cache_decorator)
    
    def test_get_cache_decorator(self):
        g.counter += 1
        return 'Counter=%s' % g.counter
    test_get_cache_decorator = beaker_cache(key="param", query_args=True)(test_get_cache_decorator)
    
    def test_expire_cache_decorator(self):
        g.counter += 1
        return 'Counter=%s' % g.counter
    test_expire_cache_decorator = beaker_cache(expire=4)(test_expire_cache_decorator)
    
    def test_key_cache_decorator(self, id):
        g.counter += 1
        return 'Counter=%s, id=%s' % (g.counter, id)
    test_key_cache_decorator = beaker_cache(key="id")(test_key_cache_decorator)
    
    def test_keyslist_cache_decorator(self, id, id2="123"):
        g.counter += 1
        return 'Counter=%s, id=%s' % (g.counter, id)
    test_keyslist_cache_decorator = beaker_cache(key=["id", "id2"])(test_keyslist_cache_decorator)
    

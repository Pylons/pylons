from pylons import app_globals
from pylons.decorators.cache import beaker_cache
from projectname.lib.base import BaseController

class CacheController(BaseController):

    @beaker_cache(key=None)
    def test_default_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter

    @beaker_cache(key="param", query_args=True)
    def test_get_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter

    @beaker_cache(expire=4)
    def test_expire_cache_decorator(self):
        app_globals.counter += 1
        return 'Counter=%s' % app_globals.counter

    @beaker_cache(key="id")
    def test_key_cache_decorator(self, id):
        app_globals.counter += 1
        return 'Counter=%s, id=%s' % (app_globals.counter, id)

    @beaker_cache(key=["id", "id2"])
    def test_keyslist_cache_decorator(self, id, id2="123"):
        app_globals.counter += 1
        return 'Counter=%s, id=%s' % (app_globals.counter, id)

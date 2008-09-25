import time

from projectname.tests import *

class TestCacheController(TestController):
    
    def test_default_cache_decorator(self):
        response = self.app.get(url(controller='cache', action='test_default_cache_decorator'))
        assert 'Counter=1' in response

        response = self.app.get(url(controller='cache', action='test_default_cache_decorator'))
        assert 'Counter=1' in response
        
        response = self.app.get(url(controller='cache', action='test_get_cache_decorator', param="123"))
        assert 'Counter=2' in response
        response = self.app.get(url(controller='cache', action='test_get_cache_decorator', param="123"))
        assert 'Counter=2' in response
        
        response = self.app.get(url(controller='cache', action='test_expire_cache_decorator'))
        assert 'Counter=3' in response
        response = self.app.get(url(controller='cache', action='test_expire_cache_decorator'))
        assert 'Counter=3' in response
        time.sleep(8)
        response = self.app.get(url(controller='cache', action='test_expire_cache_decorator'))
        assert 'Counter=4' in response
        
        response = self.app.get(url(controller='cache', action='test_key_cache_decorator', id=1))
        assert 'Counter=5' in response
        response = self.app.get(url(controller='cache', action='test_key_cache_decorator', id=2))
        assert 'Counter=6' in response
        response = self.app.get(url(controller='cache', action='test_key_cache_decorator', id=1))
        assert 'Counter=5' in response
        
        response = self.app.get(url(controller='cache', action='test_keyslist_cache_decorator', id=1, id2=2))
        assert 'Counter=7' in response
        response = self.app.get(url(controller='cache', action='test_keyslist_cache_decorator', id=1, id2=2))
        assert 'Counter=7' in response
       

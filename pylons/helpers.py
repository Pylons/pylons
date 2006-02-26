""""Magic" helper objects (``session``, ``request``, ``m``) and ``etag_cache``

Additional helper object available for use in Controllers is the etag_cache.

These helper objects provide convenient proxy access to the thread-local objects a web
developer will want to use frequently. Any thread-local object can easily be proxy'd by
sub-classing ObjectProxy and providing a ``_get_object`` method that will retrieve the
desired thread-local for access.
"""

from myghty import request
import pylons

class ObjectProxy(object):
    """Proxy access to an object
    
    ObjectProxy provides direct access to an object that normally
    requires a function call of some sort to retrieve.
    """
    def _get_object(self):
        raise NotImplementedError()
    
    def __getitem__(self, key):
        return self._get_object()[key]
    
    def __setitem__(self, key, value):
        self._get_object()[key] = value

    def __delitem__(self, key):
        self._get_object().__delitem__(key)
    
    def __getattr__(self, name):
        return getattr(self._get_object(), name)
    
    def __setattr__(self, name, value):
        setattr(self._get_object(), name, value)

    def __delattr__(self, name):
        self._get_object().__delattr__(name)
    
    def __repr__(self):
        return self._get_object().__repr__()
    
    def __iter__(self):
        return iter(self._get_object().keys())
    

class SessionProxy(ObjectProxy):
    """Retrieves the session thread-local from the Myghty request"""
    def _get_object(self):
        inst = request.instance()
        return inst.get_session()

class RequestProxy(ObjectProxy):
    """Retrieves the http request object from the Myghty request"""
    def _get_object(self):
        inst = request.instance()
        return inst.request_impl.httpreq

class MyghtyProxy(ObjectProxy):
    """Retrieves the Myghty request object from the Myghty thread-local"""
    def _get_object(self):
        return request.instance()

class GlobalsProxy(ObjectProxy):
    """Retrieves the environ globals var pylons.g"""
    def _get_object(self):
        req = request.instance().request_impl.httpreq
        return req.environ['pylons.g']

class RequestArgProxy(ObjectProxy):
    """Retrieves the request args from the Myghty request object"""
    def _get_object(self):
        inst = request.instance()
        return inst.request_args
        

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to the response for use in future
    request cycles.
    
    Suggested use is within a Controller Action like so::
    
        import pylons
        
        class YourController(BaseController):
            def index(self):
                if pylons.etag_cache(key=1): return
                m.subexec('/splash.myt')
    
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    pylons.request.headers_out['ETag'] = key
    if str(key) == if_none_match:
        pylons.m.abort(304)
        return True
    else:
        return False

__all__ = ['SessionProxy', 'RequestProxy', 'MyghtyProxy', 'GlobalsProxy', 'etag_cache', 'RequestArgProxy']

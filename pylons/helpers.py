""""``etag_cache``

Additional helper object available for use in Controllers is the etag_cache.

"""
import pylons

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

__all__ = ['etag_cache']

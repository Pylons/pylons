"""Caching decorator"""
import inspect
import logging
import time

from decorator import decorator
from paste.deploy.converters import asbool

try:
    import set
except:
    from sets import Set as set
    
log = logging.getLogger(__name__)

def beaker_cache(key="cache_default", expire="never", type=None,
                 query_args=False,
                 cache_headers=('content-type', 'content-length'),
                 invalidate_on_startup=False, **b_kwargs):
    """Cache decorator utilizing Beaker. Caches action or other
    function that returns a pickle-able object as a result.

    Optional arguments:

    ``key``
        None - No variable key, uses function name as key
        "cache_default" - Uses all function arguments as the key
        string - Use kwargs[key] as key
        list - Use [kwargs[k] for k in list] as key
    ``expire``
        Time in seconds before cache expires, or the string "never". 
        Defaults to "never"
    ``type``
        Type of cache to use: dbm, memory, file, memcached, or None for
        Beaker's default
    ``query_args``
        Uses the query arguments as the key, defaults to False
    ``cache_headers``
        A tuple of header names indicating response headers that
        will also be cached.
    ``invalidate_on_startup``
        If True, the cache will be invalidated each time the application
        starts or is restarted.

    If cache_enabled is set to False in the .ini file, then cache is
    disabled globally.

    """
    if invalidate_on_startup:
        starttime = time.time()
    else:
        starttime = None
    cache_headers = set(cache_headers)

    def wrapper(func, *args, **kwargs):
        """Decorator wrapper"""
        self = args[0]
        log.debug("Wrapped with key: %s, expire: %s, type: %s, query_args: %s",
                  key, expire, type, query_args)
        enabled = self._py_object.config.get("cache_enabled", "True")
        if not asbool(enabled):
            log.debug("Caching disabled, skipping cache lookup")
            return func(*args, **kwargs)

        if key:
            if query_args:
                key_dict = dict(self._py_object.request.GET)
            else:
                key_dict = kwargs.copy()
                key_dict.update(_make_dict_from_args(func, args))
            
            if key != "cache_default":
                if isinstance(key, list):
                    key_dict = dict((k, key_dict[k]) for k in key)
                else:
                    key_dict = {key: key_dict[key]}
        else:
            key_dict = None

        namespace, cache_key = create_cache_key(func, key_dict, self)
        my_cache = self._py_object.cache.get_cache(namespace)

        if expire == "never":
            cache_expire = None
        else:
            cache_expire = expire
        
        def create_func():
            log.debug("Creating new cache copy with key: %s, type: %s",
                      cache_key, type)
            result = func(*args, **kwargs)
            glob_response = self._py_object.response
            headers = glob_response.headerlist
            status = glob_response.status
            full_response = dict(headers=headers, status=status,
                                 cookies=None, content=result)
            return full_response
        
        if type:
            b_kwargs['type'] = type

        response = my_cache.get_value(cache_key, createfunc=create_func,
                                     expiretime=cache_expire, starttime=starttime,
                                     **b_kwargs)
        
        glob_response = self._py_object.response
        glob_response.headerlist = [header for header in response['headers'] if header[0].lower() in cache_headers]
        glob_response.status = response['status']

        return response['content']
    return decorator(wrapper)

def create_cache_key(func, key_dict=None, self=None):
    """Get a cache namespace and key used by the beaker_cache decorator.
    
    Example::
        from pylons import cache
        from pylons.decorators.cache import create_cache_key
        namespace, key = create_cache_key(MyController.some_method)
        cache.get_cache(namespace).remove(key)
            
    """
    if key_dict:
        cache_key = " ".join(["%s=%s" % (k, v) for k, v in key_dict.iteritems()])
    else:
        if hasattr(self, 'im_func'):
            cache_key = func.im_func.__name__
        else:
            cache_key = func.__name__
    
    if self:
        return '%s.%s' % (func.__module__, self.__class__.__name__), cache_key
    else:
        return '%s.%s' % (func.__module__, func.im_class.__name__), cache_key

def _make_dict_from_args(func, args):
    """Inspects function for name of args"""
    args_keys = {}
    for i, arg in enumerate(inspect.getargspec(func)[0]):
        if arg != "self":
            args_keys[arg] = args[i]
    return args_keys

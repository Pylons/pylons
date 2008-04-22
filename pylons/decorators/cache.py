"""Caching decorator"""
import inspect
import logging

from decorator import decorator
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

def beaker_cache(key="cache_default", expire="never", type=None,
    query_args=False, response=False, **b_kwargs):
    """Cache decorator utilizing Beaker. Caches action or other
    function that returns a pickle-able object as a result.

    Optional arguments:

    ``key``
        None - No variable key, uses function name as key
        "cache_default" - Uses all function arguments as the key
        string - Use kwargs[key] as key
        list - Joins the arguments in the list
    ``expire``
        Time in seconds before cache expires, defaults to never
    ``type``
        Type of cache to use: dbm, memory, file, memcached, or None for
        Beaker's default
    ``query_args``
        Uses the query arguments as the key, defaults to False
    ``response``
        Whether or not the response status/headers/cookies present at 
        the time the cache is generated should be restored. This is
        ideal for caching controller actions, but shouldn't be used
        for caching non-action functions. Defaults to False.

    If cache_enabled is set to False in the .ini file, then cache is
    disabled globally.
    
    """
    def wrapper(func, *args, **kwargs):
        """Decorator wrapper"""
        self = args[0]
        log.debug("Wrapped with key: %s, expire: %s, type: %s, query_args: %s",
                  key, expire, type, query_args)
        enabled = self._py_object.config.get("cache_enabled", "True")
        if not asbool(enabled):
            log.debug("Caching disabled, skipping cache lookup")
            return func(*args, **kwargs)

        my_cache = self._py_object.cache.get_cache('%s.%s' % (func.__module__,
                                                              func.__name__))
        cache_key = _make_key(func, key, args, kwargs, query_args)

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
            cookies=None
            full_response = dict(headers=headers, status=status,
                                 cookies=cookies, content=result)
            return full_response
        
        if type:
            b_kwargs['type'] = type
        
        response = my_cache.get_value(cache_key, createfunc=create_func,
                                     expiretime=cache_expire, **b_kwargs)
        if response:
            glob_response = self._py_object.response
            glob_response.headerlist = response['headers']
            glob_response.status = response['status']
        return response['content']
    return decorator(wrapper)

def _make_key(func, key, args, kwargs, query_args):
    """Helps make unique key from largs, kwargs and request.GET"""
    self = args[0]
    if key == "cache_default":
        if query_args:
            cache_key = repr(dict(self._py_object.request.GET))
        else:
            cache_key = repr(kwargs.items())
            largs_keys = _make_dict_from_args(func, args)
            cache_key += repr(largs_keys.items())
    elif not key:
        cache_key = func.__name__
    else:
        if query_args:
            dic = self._py_object.request.GET
        else:
            largs_keys = _make_dict_from_args(func, args)
            dic = kwargs.copy()
            dic.update(largs_keys)
        if isinstance(key, list):
            cache_key = " ".join(["%s=%s" % (k, dic[k]) for k in key])
        else:
            cache_key = "%s=%s" % (key, dic[key])
    return cache_key

def _make_dict_from_args(func, args):
    """Inspects function for name of args"""
    args_keys = {}
    for i, arg in enumerate(inspect.getargspec(func)[0]):
        if arg != "self":
            args_keys[arg] = args[i]
    return args_keys

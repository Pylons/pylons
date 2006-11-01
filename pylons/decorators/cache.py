"""Caching decorators"""
import inspect

from paste.deploy.converters import asbool

import pylons
from pylons.decorator import decorator

def beaker_cache(key="cache_default", expire="never", type="dbm", 
    query_args=False):
    """Cache decorator utilizing Beaker. Caches action or other function that
    returns a pickle-able object as a result.
    
    Optional arguments:
    
    key
        None - No variable key, uses function name as key
        "cache_default" - Uses all function arguments as the key
        string - Use kwargs[key] as key
        list - Joins the arguments in the list
    expire
        Time in seconds before cache expires, defaults to never
    type
        Type of cache to use: dbm, memory, file, memcached
    query_args
        Uses the query arguments as the key, defaults to False

    If cache_enabled is set to False in the .ini file, then cache is disabled 
    globally.
    """
    def wrapper(func, *args, **kwargs):
        """Decorator wrapper"""
        enabled = pylons.g.pylons_config.app_conf.get("cache_enabled", "True")
        if not asbool(enabled):
            return func(*args, **kwargs)
        
        my_cache = pylons.cache.get_cache(func.__module__ + "." + func.__name__)
        cache_key = _make_key(func, key, args, kwargs, query_args)
        
        if expire == "never":
            cache_expire = None
        else:
            cache_expire = expire
        
        content = my_cache.get_value(cache_key,
            createfunc=lambda: func(*args, **kwargs), type=type,
            expiretime=cache_expire)
        return content
    return decorator(wrapper)

def _make_key(func, key, args, kwargs, query_args):
    """Helps make unique key from largs, kewargs and request.GET"""
    if key == "cache_default":
        if query_args:
            cache_key = repr(dict(pylons.request.GET))
        else:
            cache_key = repr(kwargs.items())
            largs_keys = _make_dict_from_args(func, args)
            cache_key += repr(largs_keys.items())
    elif not key:
        cache_key = func.__name__
    else:
        if query_args:
            dic = pylons.request.GET
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

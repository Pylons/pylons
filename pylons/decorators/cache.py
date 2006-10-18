"""Caching decorators"""
import inspect
import pylons
from pylons.decorator import decorator

def response_cache(key="cache_default", expire="never", type="dbm", GET=False):
    """Cache decorator. Caches action or other function that returns a 
    pickle-able object.
    
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
    GET
        Uses the GET (query) arguments as the key, defaults to False

    If cache_enabled is set to False in the .ini file, then cache is disabled globaly
    """
    def wrapper(f, *args, **kw):
        enabled = pylons.g.pylons_config.app_conf.get("cache_enabled", "True")
        if enabled == "False":
            return f(*args, **kw)
        
        my_cache = pylons.cache.get_cache(f.__module__ + "." + f.__name__)
        cache_key = _make_key(f, key, args, kw, GET)
        
        if expire == "never":
            cache_expire = None
        else:
            cache_expire = expire
        
        content = my_cache.get_value(cache_key,
            createfunc=lambda: f(*args, **kw), type=type,
            expiretime=cache_expire)
        return content
    return decorator(wrapper)

def _make_key(f, key, args, kwargs, GET):
    """Helps make unique key from largs, kewargs and request.GET"""
    if key == "cache_default":
        if GET == True:
            cache_key = repr(dict(request.GET))
        else:
            cache_key = repr(kwargs.items())
            largs_keys = _make_dict_from_args(f, args)
            cache_key += repr(largs_keys.items())
    elif key == None:
        cache_key = f.__name__
    else:
        if GET == True:
            dic = request.GET
        else:
            largs_keys = _make_dict_from_largs(f, largs)
            dic = kwargs.copy()
            dic.update(largs_keys)
        if isinstance(key, list):
            cache_key = " ".join(["%s=%s" % (k, dic[k]) for k in key])
        else:
            cache_key = "%s=%s" % (key, dic[key])
    return cache_key

def _make_dict_from_args(f, args):
    """Inspects function for name of args"""
    args_keys = {}
    for i, arg in enumerate(inspect.getargspec(f)[0]):
        if arg != "self":
            args_keys[arg] = args[i]
    return args_keys

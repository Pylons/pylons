.. _sessions:

========
Sessions
========

Inevitably, there will be occasions during your applications development or deployment where some task takes a significant amount of time to complete. When this occurs, the best way to speed things up is with :term:`caching`. 

Pylons comes with caching middleware enabled that is part of the same package that provides the session handling, `Beaker <http://beaker.groovie.org>`_. It supports backends in memory, the filesystem, and memcached. 

There are several ways to cache data under Pylons, depending on where the slowdown is occurring:

* Browser-side Caching - HTTP/1.1 supports the :term:`ETag` caching system that allows the browser to use its own cache instead of requiring the re-generation the entire page. ETag-based caching avoids repeated generation of content but if the browser has never seen the page it will still be generated. Therefore using ETag caching in conjunction with one of the other types of caching listed here will achieve optimal throughput and avoid resource-intensive operations.

    .. Note:: the latter only helps if the entire page can be cached.

* Controllers - The `cache` object is available in controllers and templates for use in caching anything that can be pickled. 

* Templates - You can cache the results of an entire rendered template using the `3 cache keyword arguments to the render calls <http://pylonshq.com/docs/class-pylons.templating.Buffet.html#render>`_. These render commands can also be used inside templates. 

* Mako/Myghty Templates - Built-in caching options are available for both `Mako <http://www.makotemplates.org/docs/caching.html>`_ and `Myghty <http://www.myghty.org/docs/cache.myt>`_ template engines. They allow fine grained caching of only certain sections of the template, as well as caching of the entire template. 

The two primary concepts to keep in mind when caching is that caches have a *namespace* and can have *keys* under that namespace. Consider that for a single template, there might be multiple versions of the template you wish to keep a cache for. The keys in the namespace are the "version" and the name of the template is the "namespace". **Both of these values must be Python strings.** 

In templates, the cache "namespace" will be set to the name of the template being rendered automatically. Nothing else is required for caching, unless you wish to control how long the template is cached for, and have multiple versions of the template cached. 

see also Stephen Pierzchala's `Caching for Performance <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_ (stephen@pierzchala.com)

Using the Cache object 
---------------------- 

Inside a controller, the `cache` object will be available. If you have an action 
or block of code that is resource or time intensive, it can be handy to cache 
the result. The `cache` object can cache any Python structure that can be 
`pickled <http://docs.python.org/lib/module-pickle.html>`_. 

Consider an action where you'd like to cache some code that does a 
time-consuming or resource intensive lookup and returns an object that can be 
pickled (list, dict, tuple, etc.): 

.. code-block:: python 

    def some_action(self, day): 
        # hypothetical action that uses a 'day' variable as its key 

        def expensive_function(): 
            # do something that takes a lot of cpu/resources 

        # Get a cache for a specific namespace, you can name it whatever 
        # you want, in this case its 'my_function' 
        mycache = cache.get_cache('my_function') 

        # Get the value, this will create the cache copy the first time 
        # and any time it expires (in seconds, so 3600 = one hour) 
        c.myvalue = mycache.get_value(key=day, createfunc=expensive_function, 
        type="memory", expiretime=3600) 

        return render('/some/template.myt') 

The `createfunc` option requires a callable object (function) which is then called by the cache anytime a value for the provided is not in the cache, or has expired in the cache. Since it is called with no arguments, the expensive function must not require any as well. 

Other Cache Options 
^^^^^^^^^^^^^^^^^^^

The cache also supports removing values from the cache by their key, and clearing the cache should you wish to reset it. 

.. code-block:: python 

    # Clear the cache 
    mycache.clear() 

    # Remove a specific key 
    mycache.remove_value('some_key') 


Using Cache keywords to `render` 
-------------------------------- 

All `render` commmands have caching functionality built in. To use it, merely
add the appropriate cache keyword to your `render` call. 

.. code-block:: python 

    class SampleController(BaseController): 

        def index(self): 
            # Cache the template for 10 mins 
            return render('/index.myt', cache_expire=600) 

        def show(self, id): 
            # Cache this version of the template for 3 mins 
            return render('/show.myt', cache_key=id, cache_expire=180) 

        def feed(self): 
            # Cache for 20 mins to memory 
            return render('/feed.myt', cache_type='memory', cache_expire=1200) 

        def home(self, user): 
            # Cache this version of a page forever (until the cache dir is cleaned) 
            return render('/home.myt', cache_key=user, cache_expire='never') 


Using the Cache Decorator 
-------------------------

Pylons also provides the `beaker_cache 
<http://pylonshq.com/docs/module-pylons.decorators.cache.html#beaker_cache>`_ 
decorator for caching the results of an entire function call (memoizing) to 
`pylons.cache`. 

It takes the same cache arguments (minus their `cache_` prefix) as does the 
`render` function. 

.. code-block:: python 

    from pylons.decorators.cache import beaker_cache 

    class SampleController(BaseController): 

        # Cache this controller action forever (until the cache dir is cleaned) 
        @beaker_cache() 
        def home(self): 
            c.data = expensive_call() 
            return render('/home.myt') 

        # Cache this controller action by its GET args for 10 mins to memory 
        @beaker_cache(expire=600, type='memory', query_args=True) 
        def show(self, id): 
            c.data = expensive_call(id) 
            return render('/show.myt') 

By default it uses all of the decorated function's arguments as the cache 
key. It can alternatively use the `request.GET` query args as the cache key 
when the `query_args` option is enabled. The cache key can be further 
customized via the `key` argument. 

ETag Caching 
------------

Caching via ETag involves sending the browser an ETag header so that it knows 
to save and possibly use a cached copy of the page from its own cache, instead 
of your application sending it another. 

Since the ETag cache relies on sending headers to the browser, it works in a 
slightly different manner. The `etag_cache` function will return a `Response` 
object with the proper HTTP headers set if the browser doesn't yet have a copy 
of the page. Otherwise a 304 HTTP Exception will be thrown that is caught by 
Paste middlware and turned into a proper 304 response to the browser. This will
cause the browser to use its own copy. 

ETag based caching requires a single key, which is sent in the ETag HTTP header
back to the browser. The `RFC specification for HTTP headers <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_ indicates that your 
ETag header merely needs to be a string. This value does not need to be unique 
for every URL, as the browser determines whether to use its own copy based on 
the URL and the ETag key. 

.. code-block:: python 

    def my_action(self): 
        etag_cache('somekey') 
        return render('/show.myt', cache_expire=3600) 

Or to change other aspects of the response: 

.. code-block:: python 

    def my_action(self): 
        etag_cache('somekey') 
        response.headers['content-type'] = 'text/plain' 
        return render('/show.myt', cache_expire=3600) 

.. note:: 
    In this example that we're using template caching in addition to ETag
    caching. If a new visitor comes to the site, we avoid re-rendering the
    template if a cached copy exists, and repeat hits to the page by that user
    will then trigger the ETag cache. This example also will never change the
    ETag key, so the browsers cache will always be used if it has one.

Your ETag cache key will likely change depending on how often you want to have 
the browser fetch a fresh copy of the page. 

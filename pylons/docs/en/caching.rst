.. _caching:

=======
Caching
=======

Inevitably, there will be occasions during applications development or deployment when some task is revealed to be taking a significant amount of time to complete. When this occurs, the best way to speed things up is with :term:`caching`. 

Pylons comes with caching middleware enabled that is part of the same package that provides the session handling, `Beaker <http://beaker.groovie.org>`_. Beaker supports a variety of caching backends: memory-based, filesystem-based and the specialised `memcached` library. 

There are several ways to cache data under Pylons, depending on where the slowdown is occurring:

* Browser-side Caching - HTTP/1.1 supports the :term:`ETag` caching system that allows the browser to use its own cache instead of requiring regeneration of the entire page. ETag-based caching avoids repeated generation of content but if the browser has never seen the page before, the page will still be generated. Therefore using ETag caching in conjunction with one of the other types of caching listed here will achieve optimal throughput and avoid unnecessary calls on resource-intensive operations.

.. note:: the latter only helps if the entire page can be cached.

* Controllers - The `cache` object can be imported in controllers used for caching anything in Python that can be pickled.

* Templates - The results of an entire rendered template can be cached using the `3 cache keyword arguments to the render calls <pylons.templating.render_mako>`_. These render commands can also be used inside templates. 

* Mako/Myghty Templates - Built-in caching options are available for both `Mako <http://www.makotemplates.org/docs/caching.html>`_ and `Myghty <http://www.myghty.org/docs/cache.myt>`_ template engines. They allow fine-grained caching of only certain sections of the template as well as caching of the entire template. 

The two primary concepts to bear in mind when caching are i) caches have a *namespace* and ii) caches can have *keys* under that namespace. The reason for this is that, for a single template, there might be multiple versions of the template each requiring its own cached version. The keys in the namespace are the ``version`` and the name of the template is the ``namespace``. **Both of these values must be Python strings.** 

In templates, the cache ``namespace`` will automatically be set to the name of the template being rendered. Nothing else is required for basic caching, unless the developer wishes to control for how long the template is cached and/or maintain caches of multiple versions of the template. 

.. seealso::
    
    Stephen Pierzchala's `Caching for Performance <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_ (stephen@pierzchala.com)

Using the Cache object 
---------------------- 

Inside the controller, the `cache` object needs to be imported before being
used. If an action or block of code makes heavy use of resources or take a
long time to complete, it can be convenient to cache the result. The `cache`
object can cache any Python structure that can be `pickled <http://docs.python.org/lib/module-pickle.html>`_. 

Consider an action where it is desirable to cache some code that does a 
time-consuming or resource-intensive lookup and returns an object that can be 
pickled (list, dict, tuple, etc.):

.. code-block:: python
    
    # Add to existing imports
    from pylons import cache
    
    
    # Under the controller class
    def some_action(self, day): 
        # hypothetical action that uses a 'day' variable as its key 

        def expensive_function(): 
            # do something that takes a lot of cpu/resources
            return expensive_call()

        # Get a cache for a specific namespace, you can name it whatever 
        # you want, in this case its 'my_function' 
        mycache = cache.get_cache('my_function', type="memory") 

        # Get the value, this will create the cache copy the first time 
        # and any time it expires (in seconds, so 3600 = one hour) 
        c.myvalue = mycache.get_value(key=day, createfunc=expensive_function, 
                                      expiretime=3600)

        return render('/some/template.myt')

The `createfunc` option requires a callable object or a function which is then called by the cache whenever a value for the provided key is not in the cache, or has expired in the cache. 

Because the `createfunc` is called with no arguments, the resource- or time-expensive function must correspondingly also not require any arguments.

Other Cache Options 
^^^^^^^^^^^^^^^^^^^

The cache also supports the removal values from the cache, using the key(s) to identify the value(s) to be removed and it also supports clearing the cache completely, should it need to be reset.

.. code-block:: python 

    # Clear the cache 
    mycache.clear() 

    # Remove a specific key 
    mycache.remove_value('some_key') 


Using Cache keywords to `render` 
-------------------------------- 

.. warning:: Needs to be extended to cover the specific render_* calls introduced in Pylons 0.9.7

All :func:`render <pylons.templating.render_mako>` commands have caching
functionality built in. To use it, merely add the appropriate cache keyword
to the render call. 

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
            # Cache this version of a page forever (until the cache dir
            # is cleaned)
            return render('/home.myt', cache_key=user, cache_expire='never') 


Using the Cache Decorator 
-------------------------

Pylons also provides the :func:`~pylons.decorators.cache.beaker_cache`
decorator for caching in `pylons.cache` the results of a completed function call (memoizing).

The cache decorator takes the same cache arguments (minus their `cache_` prefix), as the `render` function does. 

.. code-block:: python 

    from pylons.decorators.cache import beaker_cache 

    class SampleController(BaseController): 

        # Cache this controller action forever (until the cache dir is
        # cleaned)
        @beaker_cache() 
        def home(self): 
            c.data = expensive_call() 
            return render('/home.myt') 

        # Cache this controller action by its GET args for 10 mins to memory
        @beaker_cache(expire=600, type='memory', query_args=True) 
        def show(self, id): 
            c.data = expensive_call(id) 
            return render('/show.myt') 

By default the decorator uses a composite of all of the decorated function's arguments as the cache key. It can alternatively use a composite of the `request.GET` query args as the cache key when the `query_args` option is enabled.

The cache key can be further customized via the `key` argument.


Caching Arbitrary Functions
---------------------------

Arbitrary functions can use the :func:`~pylons.decorators.cache.beaker_cache`
decorator, but should include an additional option. Since the decorator caches
the :term:`response` object, its unlikely the status code and headers for
non-controller methods should be cached. To avoid caching that data, the
cache_response keyword argument should be set to false.

.. code-block:: python
    
    from pylons.decorators.cache import beaker_cache
    
    @beaker_cache(expire=600, cache_response=False)
    def generate_data():
        # do expensive data generation
        return data

.. warning::
    
    When caching arbitrary functions, the ``query_args`` argument should not
    be used since the result of arbitrary functions shouldn't depend on
    the request parameters.

ETag Caching 
------------

Caching via ETag involves sending the browser an ETag header so that it knows 
to save and possibly use a cached copy of the page from its own cache, instead 
of requesting the application to send a fresh copy. 

Because the ETag cache relies on sending headers to the browser, it works in a 
slightly different manner to the other caching mechanisms described above. 

The :func:`~pylons.controllers.util.etag_cache` function will set the proper HTTP headers if
the browser doesn't yet have a copy of the page. Otherwise, a 304 HTTP
Exception will be thrown that is then caught by Paste middleware and
turned into a proper 304 response to the browser. This will cause the
browser to use its own locally-cached copy.

:func:`~pylons.controllers.util.etag_cache` returns 
:class:`~pylons.controllers.util.Response` for legacy purposes
(:class:`~pylons.controllers.util.Response` should be used directly instead).

ETag-based caching requires a single key which is sent in the ETag HTTP header
back to the browser. The `RFC specification for HTTP headers <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_ indicates that an 
ETag header merely needs to be a string. This value of this string does not need 
to be unique for every URL as the browser itself determines whether to use its own 
copy, this decision is based on the URL and the ETag key. 

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
    In this example that we are using template caching in addition to ETag
    caching. If a new visitor comes to the site, we avoid re-rendering the
    template if a cached copy exists and repeat hits to the page by that user
    will then trigger the ETag cache. This example also will never change the
    ETag key, so the browsers cache will always be used if it has one.

The frequency with which an ETag cache key is changed will depend on the web 
application and the developer's assessment of how often the browser should be 
prompted to fetch a fresh copy of the page. 

.. warning:: Stolen from Philip Cooper's `OpenVest wiki <http://www.openvest.com/trac/wiki/BeakerCache>`_  after which it was updated and edited ...

Inside the Beaker Cache
-----------------------

Caching
^^^^^^^

First lets start out with some **slow** function that we would like to cache.  This function is not slow but it will show us when it was cached so we can see things are working as we expect:

.. code-block:: python

    import time
    def slooow(myarg):
      # some slow database or template stuff here
      return "%s at %s" % (myarg,time.asctime())

When we have the cached function, multiple calls will tell us whether are seeing a cached or a new version.

DBMCache
^^^^^^^^

The DBMCache stores (actually pickles) the response in a dbm style database.

What may not be obvious is that there are two levels of keys.  They are essentially created as one for the function or template name (called the namespace) and one for the ''keys'' within that (called the key).  So for `Some_Function_name`, there is a cache created as one dbm file/database.  As that function is called with different arguments, those arguments are keys within the dbm file. First let's create and populate a cache.  This cache might be a cache for the function `Some_Function_name` called three times with three different arguments: `x`, `yy`, and `zzz`:

.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)

Nothing much new yet.  After getting the cache we can use the cache as per the Beaker Documentation.

.. code-block:: python

    import beaker.container as container
    cc = container.ContainerContext()
    nsm = cc.get_namespace_manager('Some_Function_name',
                                   container.DBMContainer,data_dir='beaker.cache')
    filename = nsm.file

Now we have the file name.  The file name is a `sha` hash of a string which is a join of the container class name and the function name (used in the `get_cache` function call).  It would return something like:


.. code-block:: python

    'beaker.cache/container_dbm/a/a7/a768f120e39d0248d3d2f23d15ee0a20be5226de.dbm'

With that file name you could look directly inside the cache database (but only for your education and debugging experience, **not** your cache interactions!)

.. code-block:: python

    ## this file name can be used directly (for debug ONLY)
    import anydbm
    import pickle
    db = anydbm.open(filename)
    old_t, old_v = pickle.loads(db['zzz'])

The database only contains the old time and old value.  Where did the expire time and the function to create/update the value go?.  They never make it to the database.  They reside in the `cache` object returned from `get_cache` call above.  

Note that the createfunc, and expiretime values are stored during the first call to `get_value`. Subsequent calls with (say) a different expiry time will **not** update that value.  This is a tricky part of the caching but perhaps is a good thing since different processes may have different policies in effect.

If there are difficulties with these values, remember that one call to :func:`cache.clear` resets everything.

Database Cache
^^^^^^^^^^^^^^

Using the `ext:database` cache type.

.. code-block:: python

    from beaker.cache import CacheManager
    #cm = CacheManager(type='dbm', data_dir='beaker.cache')
    cm = CacheManager(type='ext:database', 
                      url="sqlite:///beaker.cache/beaker.sqlite",
                      data_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)


This is identical to the cache usage above with the only difference being the creation of the `CacheManager`.  It is much easier to view the caches outside the beaker code (again for edification and debugging, not for api usage).

SQLite was used in this instance and the SQLite data file can be directly accessed using the SQLite command-line utility or the Firefox plug-in:

.. code-block:: text

    sqlite3 beaker.cache/beaker.sqlite
    # from inside sqlite:
    sqlite> .schema
    CREATE TABLE beaker_cache (
            id INTEGER NOT NULL, 
            namespace VARCHAR(255) NOT NULL, 
            key VARCHAR(255) NOT NULL, 
            value BLOB NOT NULL, 
            PRIMARY KEY (id), 
             UNIQUE (namespace, key)
    );
    select * from beaker_cache;

.. warning:: The data structure is different in Beaker 0.8 ...

.. code-block:: python

    cache = sa.Table(table_name, meta,
                     sa.Column('id', types.Integer, primary_key=True),
                     sa.Column('namespace', types.String(255), nullable=False),
                     sa.Column('accessed', types.DateTime, nullable=False),
                     sa.Column('created', types.DateTime, nullable=False),
                     sa.Column('data', types.BLOB(), nullable=False),
                     sa.UniqueConstraint('namespace')
    )


It includes the access time but stores rows on a one-row-per-namespace basis, (storing a pickled dict) rather than one-row-per-namespace/key-combination. This is a more efficient approach when the problem is handling a large number of namespaces with limited keys --- like sessions.

Memcached Cache
^^^^^^^^^^^^^^^

For large numbers of keys with expensive pre-key lookups memcached it the way to go.

If memcached is running on the the default port of 11211:

.. code-block:: python

    from beaker.cache import CacheManager
    cm = CacheManager(type='ext:memcached', url='127.0.0.1:11211',
                      lock_dir='beaker.cache')
    cache = cm.get_cache('Some_Function_name')
    # the cache is setup but the dbm file is not created until needed 
    # so let's populate it with three values:
    cache.get_value('x', createfunc=lambda: slooow('x'), expiretime=15)
    cache.get_value('yy', createfunc=lambda: slooow('yy'), expiretime=15)
    cache.get_value('zzz', createfunc=lambda: slooow('zzz'), expiretime=15)

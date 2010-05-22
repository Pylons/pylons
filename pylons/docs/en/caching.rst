.. _caching:

=======
Caching
=======

Inevitably, there will be occasions during applications development or deployment when some task is revealed to be taking a significant amount of time to complete. When this occurs, the best way to speed things up is with :term:`caching`. 

Caching is enabled in Pylons using `Beaker`_, the same package that
provides session handling. Beaker supports a variety of caching backends: in-memory, database, Google Datastore, filesystem, and memcached. Additional extensions are available that support Tokyo Cabinet,
Redis, Dynomite, and Ringo. Back-ends can be added with Beaker's extension
system.

.. seealso:: `Beaker Extension Add-ons <http://github.com/didip/beaker_extensions/tree/master>`_

Types of Caching
================

Pylons offers a variety of caching options depending on the granularity of
caching desired. Fine-grained caching down to specific sub-sections of a 
template, arbitrary Python functions, all the way up to entire controller
actions and browser-side full-page caching are available.

Available caching options (ordered by granularity, least to most specific):

* **Browser-side** - HTTP/1.1 supports the :term:`ETag` caching system that allows the browser to use its own cache instead of requiring regeneration of the entire page. ETag-based caching avoids repeated generation of content but if the browser has never seen the page before, the page will still be generated. Therefore using ETag caching in conjunction with one of the other types of caching listed here will achieve optimal throughput and avoid unnecessary calls on resource-intensive operations.

* **Controller Actions** - A Pylons controller action can have its entire
  result cached, including response headers if desired.

* **Templates** - The results of an entire rendered template can be cached using the :meth:`3 cache keyword arguments to the render calls <pylons.templating.render_mako>`. These render commands can also be used inside templates. 

* **Arbitrary Functions** - Any function can be independently cached using
  Beaker's cache decorators. This allows fine-grained caching of just the
  parts of the code that can be cached.

* **Template Fragments** - Built-in caching options are available for both `Mako`_ and `Myghty <http://www.myghty.org/docs/cache.myt>`_ template engines. They allow fine-grained caching of only certain sections of the template. This is also sometimes called fragment caching since individual fragments of a page can be cached.

Namespaces and Keys
===================

`Beaker`_ is used for caching arbitrary Python functions, template results,
and in `Mako`_ for caching individual `<def>` blocks. Browser-side caching
does *not* utilize `Beaker`_.

The two primary concepts to bear in mind when caching with `Beaker`_ are:

1. Caches have a *namespace*, this is to organize a cache such that variations
   of the same thing being cached are associated under a single place.
2. Variations of something being cached, are *keys* which are under that 
   namespace.

For example, if we want to cache a function, the function
name along with a unique name for it would be considered the *namespace*. The
arguments it takes to differentiate the output to cache, are the *keys*.

An example of caching with the :func:`~beaker.cache.cache_region` decorator::
    
    @cache_region('short_term', 'search_func')
    def get_results(search_param):
        # do something to retrieve data
        data = get_data(search_param)
        return data

    results = get_results('gophers')

In this example, the namespace will be the function name + module +
'search_func'. Since a single module might have multiple methods of the
same name you wish to cache, the :func:`~beaker.cache.cache_region` decorator
takes another argument in addition to the region to use, which is added to the
namespace.

The key in this example is the `search_param` value. For each value of it, a
separate result will be cached.

.. seealso::
    
    Stephen Pierzchala's `Caching for Performance <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_ (stephen@pierzchala.com)
    Beaker `Caching Docs <http://beaker.groovie.org/caching.html>`_

Configuring
===========

`Beaker`_'s cache options can be easily configured in the project's
INI file. Beaker's `configuration documentation
<http://beaker.groovie.org/configuration.html>`_ explains how to setup
the most common options.

The cache options specified will be used in the absence of more specific
keyword arguments to individual cache functions. Functions that support
:ref:`cache_regions` will use the settings for that region.

.. _cache_regions:

Cache Regions
-------------

Cache regions are named groupings of related options. For example, in many web applications, there might be a few cache strategies used in a company, with short-term cached objects ending up in Memcached, and longer-term cached objects stored in the filesystem or a database.

Using cache regions makes it easy to declare the cache strategies in one
place, then use them throughout the application by referencing the cache
strategy name.

Cache regions should be setup in the :file:`development.ini` file, but can
also be configured and passed directly into the `CacheManager` instance that
is created in the :file:`lib/app_globals.py` file.

Example INI section for two cache regions (put these under your `[app:main]` 
section):

.. code-block:: ini
    
    beaker.cache.regions = short_term, long_term
    beaker.cache.short_term.type = ext:memcached
    beaker.cache.short_term.url = 127.0.0.1:11211
    beaker.cache.short_term.expire = 3600

    beaker.cache.long_term.type = ext:database
    beaker.cache.long_term.url = mysql://dbuser:dbpass@127.0.0.1/cache_db
    beaker.cache.long_term.expire = 86400

This sets up two cache regions, `short_term` and `long_term`.


Browser-Side
============

Browser-side caching can utilize one of several methods. The entire page can
have cache headers associated with it to indicate to the browser that it 
should be cached. Or, using the ETag Cache header, a page can have more 
fine-grained caching rules applied.

Cache Headers
-------------

Cache headers may be set directly on the
:class:`~pylons.controllers.util.Response` object by setting the headers 
directly using the :meth:`~webob.response.Response.headers` property, or
by using the cache header helpers.

To ensure pages aren’t accidentally cached in dynamic web
applications, Pylons default behavior sets the `Pragma` and `Cache-Control` headers to 
`no-cache`. Before setting cache headers, these default values should be
cleared.

Clearing the default `no-cache` response headers::
    
    class SampleController(BaseController):
        def index(self):
            # Clear the default cache headers
            del response.headers['Cache-Control']
            del response.headers['Pragma']
            
            return render('/index.html)

Using the response cache helpers::
    
    # Set an action response to expires in 30 seconds
    class SampleController(BaseController):
        def index(self):
            # Clear the default cache headers
            del response.headers['Cache-Control']
            del response.headers['Pragma']
            
            response.cache_expires(seconds=30)
            return render('/index.html')
    
    # Set the cache-control to private with a max-age of 30 seconds
    class SampleController(BaseController):
        def index(self):
            # Clear the default cache headers
            del response.headers['Cache-Control']
            del response.headers['Pragma']
            
            response.cache_control = {'max-age': 30, 'public': True}
            return render('/index.html')
    
All of the values that can be passed to the `cache_control` property dict,
also may be passed into the `cache_expires` function call. It's recommended
that you use the `cache_expires` helper as it also sets the Last-Modified and
Expires headers to the second interval as well.

.. seealso:: `Cache Control Header RFC <http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9>`_

E-Tag Caching
-------------

Caching via ETag involves sending the browser an ETag header so that it knows 
to save and possibly use a cached copy of the page from its own cache, instead 
of requesting the application to send a fresh copy. 

Because the ETag cache relies on sending headers to the browser, it works in a 
slightly different manner to the other caching mechanisms. 

The :func:`~pylons.controllers.util.etag_cache` function will set the proper HTTP headers if
the browser doesn't yet have a copy of the page. Otherwise, a 304 HTTP
Exception will be thrown that is then caught by Paste middleware and
turned into a proper 304 response to the browser. This will cause the
browser to use its own locally-cached copy.

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
        return render('/show.myt')

The frequency with which an ETag cache key is changed will depend on the web 
application and the developer's assessment of how often the browser should be 
prompted to fetch a fresh copy of the page.


Controller Actions
==================

The :func:`~pylons.decorators.cache.beaker_cache` decorator is for caching
the results of a complete controller action.

Example:

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

.. warning::
    
    By default, the :func:`~pylons.decorators.cache.beaker_cache` decorator
    will cache the entire response object. This means the headers that were
    generated during the action will be cached as well. This can be disabled
    by providing `cache_response = False` to the decorator.

Templates
=========

All :func:`render <pylons.templating.render_mako>` commands have caching
functionality built in. To use it, merely add the appropriate cache keyword
to the render call.

.. code-block:: python 

    class SampleController(BaseController): 
        def index(self): 
            # Cache the template for 10 mins 
            return render('/index.html', cache_expire=600) 

        def show(self, id): 
            # Cache this version of the template for 3 mins 
            return render('/show.html', cache_key=id, cache_expire=180) 

        def feed(self): 
            # Cache for 20 mins to memory 
            return render('/feed.html', cache_type='memory', cache_expire=1200)

        def home(self, user): 
            # Cache this version of a page forever (until the cache dir
            # is cleaned)
            return render('/home.html', cache_key=user, cache_expire='never') 

.. note::
    
    At the moment, these functions do not support the use of cache region
    pre-defined argument sets.


Arbitrary Functions
===================

Any Python function that returns a pickle-able result can be cached using
`Beaker`_. The recommended way to cache functions is to use the
:meth:`~beaker.cache.cache_region` decorator. This decorator requires the
:ref:`cache_regions` to be configured.

Using the :meth:`~beaker.cache.cache_region` decorator::
    
    @cache_region('short_term', 'search_func')
    def get_results(search_param):
        # do something to retrieve data
        data = get_data(search_param)
        return data

    results = get_results('gophers')

.. seealso:: `Beaker Caching Documentation <http://beaker.groovie.org/caching.html>`_

Invalidating
------------

A cached function can be manually invalidated by using the
:meth:`~beaker.cache.region_invalidate` function.

Example::
    
    region_invalidate(get_results, None, 'search_func', search_param)


Fragments
=========

Individual template files, and `<def>` blocks within them can be independently 
cached. Since the caching system utilizes `Beaker`_, any available `Beaker`_
back-ends are present in `Mako`_ as well.

Example::
    
    <%def name="mycomp" cached="True" cache_timeout="30" cache_type="memory">
        other text
    </%def>

.. seealso:: `Mako Caching Documentation <http://www.makotemplates.org/docs/caching.html>`_

.. _cache: http://en.wikipedia.org/wiki/Cache
.. _Beaker: http://beaker.groovie.org
.. _Mako: http://www.makotemplates.org/
.. _sessions:

========
Sessions
========

Sessions
========

.. note:: The session code is due an extensive rewrite. It uses the Caching container API in Beaker which is optimized for use patterns that are more common in caching (infrequent updates / frequent reads). Unlike caching, a session is a single load, then a single save and multiple simultaneous writes to the same session occur only rarely. In consequence, the excessive but necessary locking that the cache interface currently performs is just a waste of performance where sessions are concerned.

Session Objects
===============

SessionObject
-------------

This session proxy / lazy creator object handles access to the real session object. If the session hasn't been used before a session object will automatically be created and set up. Using a proxy in this fashion to handle access to the real session object avoids creating and loading the session from persistent store unless it is actually used during the request.

CookieSession
-------------

Pure cookie-based session. The options recognized when using cookie-based sessions are slightly more restricted than general sessions.
    
* ``key``
    The name the cookie should be set to.
* ``timeout``
    How long session data is considered valid. This is used  regardless of the cookie being present or not to determine whether session data is still valid.
* ``encrypt_key``
    The key to use for the session encryption, if not provided the session will not be encrypted.
* ``validate_key``
        The key used to sign the encrypted session
* ``cookie_domain``
        Domain to use for the cookie.
* ``secure``
        Whether or not the cookie should only be sent over SSL.

Beaker
======

.. code-block:: ini 

    beaker.session.key = wiki 
    beaker.session.secret = ${app_instance_secret} 

Pylons comes with caching middleware enabled that is part of the same package that provides the session handling, `Beaker <http://beaker.groovie.org>`_. Beaker supports several different types of cache back-end: memory, filesystem, memcached and database. The supported database packages are: SQLite, SQLAlchemy and Google BigTable.


Beaker's cache and session options are configured via a dictionary.

.. note:: When used with the Paste package, all Beaker options should be prefixed with ``beaker.`` so that Beaker can discriminate its options from other application configuration options.


General Config Options
----------------------

Config options should be prefixed with either ``session.`` or ``cache.``

data_dir
^^^^^^^^

*Accepts:* string
*Default:* None

The data directory where cache data will be stored. If this argument is not present, the regular data_dir parameter is used, with the path "./sessions" appended to it.

type
^^^^

*Accepts:* string
*Default:* dbm

Type of storage used for the session, current types are "dbm", "file", "memcached", "database", and "memory". The storage uses the Container API that is also used by the cache system.

When using dbm files, each user's session is stored in its own dbm file, via the class :class"`beaker.container.DBMNamespaceManager` class.

When using 'database' or 'memcached', additional configuration options are required as documented in the appropriate section below.

For sessions only, there is an additional choice of a "cookie" type, which requires the Sessions "secret" option to be set as well.


Database Configuration
----------------------
When the type is set to 'database', the following additional options can be used.

url (*required*)
^^^^^^^^^^^^^^^^

*Accepts:* string (formatted as required for an `SQLAlchemy db uri`__)
*Default:* None

.. __: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_establishing

The database URI as formatted for SQLAlchemy to use for the database. The appropriate database packages for the database must also be installed.

table_name
^^^^^^^^^^

*Accepts:* string
*Default:* beaker_cache

Table name to use for beaker's storage.

optimistic
^^^^^^^^^^

*Accepts:* boolean
*Default:* False

Use optimistic session locking, note that this will result in an select when updating a cache value to compare version numbers.

sa_opts (*Only for SQLAlchemy 0.3*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Accepts:* dict
*Default:* None

A dictionary of values to use that are passed directly to SQLAlchemy's engine. Note that this is only applicable for SQLAlchemy 0.3.

sa.*
^^^^

*Accepts:* Valid `SQLAlchemy 0.4 database options`__
*Default:* None

.. __: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_options

When using SQLAlchemy 0.4 and above, all options prefixed with ``sa.`` are passed to the SQLAlchemy database engine. Common parameters are ``pool_size``, ``pool_recycle``, etc.


Memcached Options
-----------------

url (required)
^^^^^^^^^^^^^^

*Accepts:* string
*Default:* None

The url should be a single IP address, or list of semi-colon separated IP addresses that should be used for memcached.

Beaker can use either py-memcached or cmemcache to communicate with memcached, but it should be noted that cmemcache can cause Python to segfault should memcached become unreachable.


Session Options
---------------

cookie_expires
^^^^^^^^^^^^^^

*Accepts:* boolean, datetime, timedelta
*Default:* True

The expiration time to use on the session cookie. Defaults to "True" which means, don't specify any expiration time (the cookie will expire when the browser is closed). A value of "False" means, never expire (specifies the maximum date that can be stored in a datetime object and uses that). The value can also be a {{datetime.timedelta()}} object which will be added to the current date and time, or a {{datetime.datetime()}} object.

cookie_domain
^^^^^^^^^^^^^

*Accepts:* string
*Default:* The entire domain name being used, including sub-domain, etc.

By default, Beaker's sessions are set to the cookie domain of the entire hostname. For sub-domains, this should be set to the top domain the cookie should be valid for.

id
^^

*Accepts:* string
*Default:* None

Session id for this session. When using sessions with cookies, this parameter is not needed as the session automatically creates, writes and retrieves the value from the request. When using a URL-based method for the session, the id should be retreived from the id data member when the session is first created, and then used in writing new URLs.

key
^^^

*Accepts:* string
*Default:* beaker_session_id

The key that will be used as a cookie key to identify sessions. Changing this could allow several different applications to have different sessions underneath the same hostname.

secret
^^^^^^

*Accepts:* string
*Default:* None

Secret key to enable encrypted session ids. When non-None, the session ids are generated with an MD5-signature created against this value.

When used with the "cookie" Session type, the secret is used for encrypting the contents of the cookie, and should be a reasonably secure randomly generated string of characters no more than 54 characters.

timeout
^^^^^^^

*Accepts:* integer
*Default:* None

Time in seconds before the session times out. A timeout occurs when the session has not been loaded for more than timeout seconds.

Session Options (For use with cookie-based Sessions)
----------------------------------------------------

encrypt_key
^^^^^^^^^^^

*Accepts:* string
*Default:* None

The key to use for the session encryption, if not provided the session will not be encrypted. This will only work if a strong hash scheme is available, such as pycryptopp's or Python 2.5's hashlib.sha256.

validate_key
^^^^^^^^^^^^

*Accepts:* string
*Default:* None

The key used to sign the encrypted session, this is used instead of a secret option.


Custom and caching middleware
=============================

Care should be taken when deciding in which layer to place custom
middleware. In most cases middleware should be placed between the
Pylons WSGI application instantiation and the Routes middleware; however,
if the middleware should run *before* the session object or routing is handled::

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware can only see the cache object, nothing *above* here
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)

Some of the Pylons middleware layers such as the ``Session``, ``Routes``, and ``Cache`` middleware, only add
objects to the `environ` dict, or add HTTP headers to the response (the Session middleware for 
example adds the session cookie header). Others, such as the ``Status Code Redirect``, and the ``Error 
Handler`` may fully intercept the request entirely, and change how its responded to.

Bulk deletion of expired db-held sessions
=========================================

The db schema for Session stores a "last accessed time" for each session. This enables bulk deletion of expired sessions through the use of a simple SQL command, run every day, that clears those sessions which have a "last accessed" timestamp > 2 days, or whatever is required.

Using `Session` in Internationalization
=======================================

How to set the language used in a controller on the fly. 

For example this could be used to allow a user to set which language they 
wanted your application to work in. Save the value to the session object: 

.. code-block:: python 

    session['lang'] = 'en' 
    session.save() 

then on each controller call the language to be used could be read from the 
session and set in the controller's ``__before__()`` method so that the pages 
remained in the same language that was previously set: 

.. code-block:: python 

    def __before__(self): 
        if 'lang' in session: 
            set_lang(session['lang']) 


Using `Session` in Secure Forms
===============================

Authorization tokens are stored in the client's session. The web app can then
verify the request's submitted authorization token with the value in the
client's session.

This ensures the request came from the originating page. See the wikipedia entry
for `Cross-site request forgery`__ for more information.

.. __: http://en.wikipedia.org/wiki/Cross-site_request_forgery

Pylons provides an ``authenticate_form`` decorator that does this verfication
on the behalf of controllers.

These helpers depend on Pylons' ``session`` object.  Most of them can be easily 
ported to another framework by changing the API calls.

Hacking the session for no cookies
==================================

(From a `paste #441 <http://pylonshq.com/pasties/441>`_ baked by Ben Bangert)

Set the session to not use cookies in the dev.ini file

.. code-block:: ini 

    beaker.session.use_cookies = False

with this as the *mode d'emploi* in the controller action

.. code-block:: python

    from beaker.session import Session as BeakerSession

    # Get the actual session object through the global proxy
    real_session = session._get_current_obj()

    # Duplicate the session init options to avoid screwing up other sessions in 
    # other threads
    params = real_session.__dict__['_params']

    # Now set the id param used to make a session to our session maker, 
    # if id is None, a new id will be made automatically
    params['id'] = find_id_func()
    real_session.__dict__['_sess'] = BeakerSession({}, **params)

    # Now we can use the session as usual
    session['fred'] = 42
    session.save()

    # At the end, we need to see if the session was used and handle its id
    if session.is_new:
        # do something with session.id to make sure its around next time
        pass

Using middleware (Beaker) with a composite app
==============================================

How to allow called WSGI apps to share a common session management utility. 

(From a `paste #616 <http://pylonshq.com/pasties/616>`_ baked by Mark Luffel)

.. code-block:: ini 

    # Here's an example of configuring multiple apps to use a common 
    # middleware filter
    # The [app:home] section is a standard pylons app
    # The ``/servicebroker`` and ``/proxy`` apps both want to be able 
    # to use the same session management

    [server:main]
    use = egg:Paste#http
    host = 0.0.0.0
    port = 5000

    [filter-app:main]
    use = egg:Beaker#beaker_session
    next = sessioned
    beaker.session.key = my_project_key
    beaker.session.secret = i_wear_two_layers_of_socks

    [composite:sessioned]
    use = egg:Paste#urlmap
    / = home
    /servicebroker = servicebroker
    /proxy = cross_domain_proxy

    [app:servicebroker]
    use = egg:Appcelerator#service_broker

    [app:cross_domain_proxy]
    use = egg:Appcelerator#cross_domain_proxy

    [app:home]
    use = egg:my_project
    full_stack = true
    cache_dir = %(here)s/data

storing SA mapped objects in Beaker sessions
============================================

Taken from pylons-discuss Google group discussion:

.. code-block:: text 

    > I wouldn't expect a SA object to be serializable.  It just doesn't
    > make sense to me.  I don't even want to think about complications with
    > the database and ACID, nor do I want to consider the scalability
    > concerns (the SA object should be tied to a particular SA session,
    > right?).

SA objects are serializable (as long as you aren't using :func:`assign_mapper`, which can complicate things unless you define a custom  :func:`__getstate__` method).

The error above is because the entity is not being detached from its original session. If you are going to  
serialize, you have to manually shuttle the object to and from the appropriate sessions.

Three ways to get an object out of serialization and back into an SA  
session are:

1. A mapped class that has a :func:`__getstate__` which only copies desired properties and won't copy SA session pointers:

    .. code-block:: python

         beaker.put(key, obj)
         ...
         obj  = beaker.get(key)
         session.save_or_update(obj)

2. A regular old mapped class.  Add an :func:`expunge` step.

    .. code-block:: python

         session.expunge(obj)
         beaker.put(key, obj)
         ...
         obj  = beaker.get(key)
         session.save_or_update(obj)

3. Don't worry about :func:`__getstate__` or :func:`expunge` on the original object, use :func:`merge`. This is "cleaner" than the :func:`expunge` method shown above but will usually force a load of the object from the database and therefore is not necessarily as "efficient", also it copies the state of the given object to the target object which may be error-prone.

    .. code-block:: python

        beaker.put(key, obj)
        ...
        obj = beaker.get(key)
        obj = session.merge(obj)



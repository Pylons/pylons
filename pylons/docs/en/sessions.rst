.. _sessions:

========
Sessions
========

Sessions
========

Pylons includes a session object: a session is a server-side, semi-permanent
storage for data associated with a client.

The session object is provided by the `Beaker library`_ which also provides
caching functionality as described in :ref:`caching`.

The Session Object
==================

The Pylons session object is available at :data:`pylons.session`. Controller
modules created via :command:`paster controller/restcontroller` import the
session object by default.

The basic session API is simple, it implements a dict-like interface with a few
additional methods. The following is an example of using the session to store a
token identifying if a client is logged in.

.. code-block :: python

    class LoginController(BaseController):

        def authenicate(self):
            name = request.POST['name']
            password = request.POST['password']
            user = Session.query(User).filter_by(name=name,
                                                 password=password).first()
            if user:
                msg = 'Successfully logged in as %s' % name
                location = url('index')
                session['logged_in'] = True
                session.save()
            else:
                msg = 'Invalid username/password'
                location = url('login')
            flash(msg)
            redirect(location)

        def logout(self):
            # Clear all values in the session associated with the client
            session.clear()
            session.save()

Subsequent requests can then determine if a client is logged in or not by
checking the session:

.. code-block :: python 

    if not session.get('logged_in'):
        flash('Please login')
        redirect(url('login'))
        
The session object acts lazily: it does not load the session data (from disk or
whichever backend is used) until the data is first accessed. This lazyness is
facilitated via an intermediary :class:`beaker.session.SessionObject` that
wraps the actual :class:`beaker.session.Session` object. Furthermore the
session will not write changes to its backend without an explicit call to its
:meth:`beaker.session.Session.save` method (unless configured with the ``auto``
option).

Session data is generally serialized for storage via the Python :mod:`pickle`
module, so anything stored in the session must be pickleable.

The lightweight SessionObject wrapper is created by the:
:class:`beaker.middleware.SessionMiddleware` WSGI middleware. SessionMiddleware
stores the wrapper in the WSGI environ where Pylons sets a reference to it from
pylons.session.

Sessions are associated with a client via a client-side cookie. The WSGI
middleware is also responsible for sending said cookie to the client.

Configuring the Session
=======================

The basic session defaults are:

* File based sessions (session data is stored on disk)
* Session cookies have no expiration date (cookies expire at the end of the browser session)
* Session cookie domain/path matches the current host/path

Pylons projects by default sets the following couple of session options via
their .ini files. All Beaker specific session options in the ini file are
prefixed with `beaker.session`:

.. code-block :: ini

    cache_dir = %(here)s/data
    beaker.session.key = foo
    beaker.session.secret = somesecret

``cache_dir`` acts a base directory for both session and cache storage. Session
data is stored in this location under a :file:`sessions/` sub-directory.

``session.key`` is the name attribute of the cookie sent to the browser. This
defaults to your project's name.

``session.secret`` is the secret token used to hash the cookie data sent to the
client. This should be a secret, ideally randomly generated value on production
environments. :command:`paster make-config` will generate a random secret for
you when creating a production ini file.


Other Session Options
---------------------

Some other commonly used session options are:

* ``type``
  The type of the back-end for storing session data. Beaker supports many
  different backends, see `Beaker Configuration Documentation`_ for the
  choices. Defaults to 'file'.

* ``cookie_domain``
  The domain name to use for the session Cookie. For example, when using
  sub-domains, set this to the parent domain name so that the cookie is valid
  for all sub-domains.

To enable pure `Cookie-based Sessions`_ and force the cookie domain to be valid
for all sub-domains of 'example.com', add the following to your Pylons ini
file:

.. code-block :: ini

    beaker.session.type = cookie
    beaker.session.cookie_domain = .example.com

See the `Beaker Configuration Documentation`_ for an exhaustive list of Session
options.


Storing SQLAlchemy mapped objects in Beaker sessions
====================================================

Mapped objects from SQLAlchemy can be serialized into the beaker session, but
care must be taken when retrieving these objects back from the beaker
session. They will not be associated with the SQLAlchemy Unit-of-Work Session,
however these objects can be reconciled via the SQLAlchemy Session's ``merge``
method, as follows:

    .. code-block:: python

        address = DBSession.query(Address).get(id)
        session[id] = address
        ...
        address = session.get(id)
        address = DBSession.merge(address)


Custom and caching middleware
=============================

Care should be taken when deciding in which layer to place custom
middleware. In most cases middleware should be placed between the
Pylons WSGI application instantiation and the Routes middleware; however,
if the middleware should run *before* the session object or routing is handled:

.. code-block:: python

    # Routing/Session Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware can only see the cache object, nothing *above* here
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)

Some of the Pylons middleware layers such as the ``Session``, ``Routes``, and ``Cache`` middleware, only add
objects to the `environ` dict, or add HTTP headers to the response (the Session middleware for 
example adds the session cookie header). Others, such as the ``Status Code Redirect``, and the ``Error 
Handler`` may fully intercept the request entirely, and change how its responded to.

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

Pylons provides an ``authenticate_form`` decorator that does this verification
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


.. _`Beaker library`: http://beaker.groovie.org
.. _`Beaker Configuration Documentation`: http://beaker.groovie.org/configuration.html#session-options
.. _`Cookie-based Sessions`: http://beaker.groovie.org/sessions.html#cookie-based

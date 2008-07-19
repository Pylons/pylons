.. _configuration:

=============
Configuration
=============

XXX: Write overview of configuration choices, difference between run-time/deplyment configuration, and application configuration (whats in the config/ dir)

Pylons is very flexible and highly configurable. It can be configured for production and development settings, as would be expected; however, Pylons can also maintain configurations for deployment on different production-server environments as well. 

There are a number of important files in :file:`config/` including:

* :file:`config/__init__.py`
* :file:`config/environment.py`
* :file:`config/middleware.py`
* :file:`config/routing.py`

Each of these files allows developers to change the 
 
.. _run-config:

Runtime Configuration
=====================

XXX: Explain run-time config, the ini format used by development.ini and the
other ini files and how that affects the run-time configuration

.. _environment-config:

Environment
===========

The :file:`config/environment.py` module, sets up the basic Pylons environment
variables needed to run the application. Objects that should be setup once
for the entire application should either be setup here, or in the
:file:`lib/app_globals` :meth:`__init__.py` method.

It also calls the :ref:`url-config` function to setup how the URL's will
be matched up to your :ref:`controllers`, creates your :term:`app_globals`
object, configures which module will be referred to as :term:`h`, and is
where the template engine is setup.

If you're using SQLAlchemy, its recommended that you setup the SQLAlchemy
engine in this module. The default SQLAlchemy setup that Pylons comes with
creates the engine here which is then used in :file:`model/__init__.py`.


.. _url-config:

URL Configuration
=================

XXX: Explanation of how the default route can map to any controller, how to add routes, link to Routes manual

More information can be found at the `the Routes manual <http://routes.groovie.org/manual.html>`_.

.. _middleware-config:

Middleware
==========

XXX: How to change the middleware, the purpose of full_stack, changing when
middleware is used in the stack

Pylons allows developers to insert their own middleware. Within
:file:`config/middleware.py` a Pylons application is wrapped in successive
layers which add functionality. The process of wrapping the Pylons application
in middleware results in a structure conceptually similar to the layers in an
onion.

.. image:: _static/pylons_as_onion.png
   :alt: Pylons middleware onion analogy

Once the middleware has been used to wrap the Pylons application, the make_app
function returns the completed app with the following structure (outermost
layer listed first):

Registry Manager
    Status Code Redirect
        Error Handler
            Cache Middleware
                Session Middleware
                    Routes Middleware
                        Pylons App to set-up globals
                            WSGI Controller (called by Pylons app)

.. note:: 
    
    There is one final piece of middleware called Cascade which is used to
    serve static content and JavaScript files during development. Before
    placing your Pylons application into production, this line should be
    commented out.

Adding custom middleware
------------------------

Custom middleware should be included in the :file:`config/middleware.py` at
comment marker::

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

For example, if you had a middleware component named `MyMiddleware` you could
include it in :file:`config/middleware.py` as follows::

    # The Pylons WSGI app
    app = PylonsApp()
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MyMiddleware(app)
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
The app object is simply passed as a parameter to your middleware which in 
turn should return a wrapped WSGI application.

Care should be taken when deciding in which layer to place your custom
middleware. In most cases, your middleware should be placed between the
Pylons WSGI application instantiation and the Routes middleware; however,
if your middleware requires access to the Pylons Session, you may want to
nest your middleware between the SessionMiddleware and the CacheMiddleware
calls::

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    
    # MyMiddleware will now have access to SessionMiddleware
    app = MyMiddleware(app)
    
    app = CacheMiddleware(app, config)

Please consult the appropriate source for more information on the standard
Pylons middleware.

What is full_stack?
-------------------

In the Pylons ini file {:file:`development.ini` or :file:`production.ini`} this block determines if the flag full_stack is set to true or false::

    [app:main]
    use = egg:your_app_name
    full_stack = true

The full_stack flag determines if the ErrorHandler is included as a layer in the middleware wrapping process.



.. _setup-config:

Application Setup
=================

XXX: Explain how to setup app dependencies in the setup.py file to ensure
the appropriate libraries are required, explain what setup.py needs, etc.

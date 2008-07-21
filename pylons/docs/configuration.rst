.. _configuration:

=============
Configuration
=============

Pylons comes with two main ways to configure an application:

* The configuration file (:ref:`run-config`)
* The application's ``config`` directory

The files in the ``config`` directory change certain aspects of how the application behaves. Any options that the webmaster should be able to change during deployment should be specified in a configuration file.

.. tip::
    A good indicator of whether an option should be set in the ``config`` directory code vs. the configuration file is whether or not the option is necessary for the functioning of the application. If the application won't function without the setting, it belongs in the appropriate :file:`config/` directory file. If the option should be changed depending on deployment, it belongs in the :ref:`run-config`.

The applications :file:`config/` directory includes:

* :file:`config/environment.py` described in :ref:`environment-config`
* :file:`config/middleware.py` described in :ref:`middleware-config`
* :file:`config/routing.py` described in :ref:`url-config`

Each of these files allows developers to change key aspects of how the application behaves.
 
.. _run-config:

*********************
Runtime Configuration
*********************

When a new project is created a sample configuration file called :file:`development.ini` is automatically produced as one of the project files. This default configuration file contains sensible options for development use, for example when developing a Pylons application it is very useful to be able to see a debug report every time an error occurs. The :file:`development.ini` file includes options to enable debug mode so these errors are shown.

Since the configuration file is used to determine which application is run, multiple configuration files can be used to easily toggle sets of options. Typically a developer might have a ``development.ini`` configuration file for testing and a ``production.ini`` file produced by the :command:`paster make-config` command for testing the command produces sensible production output. A :file:`test.ini` configuration is also included in the project for test-specific options.

To specify a configuration file to use when running the application, change the last part of the :command:`paster serve` to include the desired config file:

.. code-block :: bash 

    $ paster serve production.ini

.. seealso::
    Configuration file format **and options** are described in great detail in the `Paste Deploy documentation <http://pythonpaste.org/deploy/>`_.


Getting Information From Configuration Files
============================================

All information from the configuration file is available in the ``pylons.config`` object. ``pylons.config`` also contains application configuration as defined in the project's :file:`config.environment` module. 

.. code-block :: python

    from pylons import config 

``pylons.config`` behaves like a dictionary. For example, if the configuration file has an entry under the ``[app:main]`` block:

.. code-block :: ini

    cache_dir = %(here)s/data

That can then be read in the projects code:

.. code-block :: python

    from pylons import config 
    cache_dir = config['cache_dir']

Or the current debug status like this: 

.. code-block :: python 

    debug = config['debug']


Production Configuration Files
==============================

To change the defaults of the configuration INI file that should be used when deploying the application, edit the :file:`config/deployment.ini_tmpl` file. This is the file that will be used as a template during deployment, so that the person handling deployment has a starting point of the minimum options the application needs set.

One of the most important options that should be changed is the ``debug = true`` setting. The email options should be setup so that errors can be e-mailed to the appropriate developers or webmaster in the event of an application error.

Generating the Production Configuration
---------------------------------------

To generate the production.ini file from the projects' :file:`config/deployment.ini_tmpl` it must first be installed either as an :term:`egg` or under development mode. Assuming the name of the Pylons application is ``helloworld``, run:

.. code-block :: bash

    $ paster make-config helloworld production.ini

.. note::
    This command will also work from inside the project when its being developed.

It is theresponsibility of the developer to ensure that a sensible set of default configuration values exist when the webmaster uses the ``paster make-config`` command. 

.. warning::
    **Always** make sure that the ``debug`` is set to ``false`` when deploying a Pylons application.


.. _environment-config:

***********
Environment
***********

The :file:`config/environment.py` module sets up the basic Pylons environment
variables needed to run the application. Objects that should be setup once
for the entire application should either be setup here, or in the
:file:`lib/app_globals` :meth:`__init__.py` method.

It also calls the :ref:`url-config` function to setup how the URL's will
be matched up to :ref:`controllers`, creates the :term:`app_globals`
object, configures which module will be referred to as :term:`h`, and is
where the template engine is setup.

When using SQLAlchemy it's recommended that the SQLAlchemy engine be setup
in this module. The default SQLAlchemy configuration that Pylons comes
with creates the engine here which is then used in :file:`model/__init__.py`.


.. _url-config:

*****************
URL Configuration
*****************

A Python library called Routes handles mapping URLs to controllers and their methods, or their :term:`action` as Routes refers to them. By default, Pylons sets up the following :term:`route`\s (found in :file:`config/routing.py`):

.. code-block:: python

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

.. versionchanged:: 0.9.7
    Prior to Routes 1.9, all map.connect statements required variable parts
    to begin with a ``:`` like ``map.connect(':controller/:action')``. This
    syntax is now optional, and the new ``{}`` syntax is recommended.

Any part of the path inside the curly braces is a variable that will match
any text in the URL for that 'part'. A 'part' of the URL is the text between
two forward slashes. Every part of the URL must be present for the
:term:`route` to match, otherwise a 404 will be returned.

.. note::
    Routes also includes the ability to attempt to 'minimize' the URL. This
    behavior is generally not intuitive, and starting in Pylons 0.9.7 is
    turned off by default with the ``map.minimization=False`` setting.

The default mapping can match to any controller and any of their
actions which means the following URLs will match:

.. code-block:: text

    /hello/index       >>    controller: hello, action: index
    /entry/view/4      >>    controller: entry, action: view, id:4
    /comment/edit/2    >>    controller: comment, action: edit, id:2

This simple scheme can be suitable for even large applications when complex URL's aren't needed.

Controllers can be organized into directories as well. For example, if the admins should have a separate ``comments`` controller:

.. code-block:: bash
    
    $ paster controller admin/comments

Will create the ``admin`` directory along with the appropriate ``comments``
controller under it. To get to the comments controller:

.. code-block:: text
    
    /admin/comments/index    >>    controller: admin/comments, action: index

Adding a route to match ``/``
=============================

The controller and action can be specified directly in the :meth:`map.connect`
statement, as well as the raw URL should be matched.

.. code-block:: python

    map.connect('/', controller='main', action='index')

will result in ``/`` being handled by the ``index`` method of the ``main``
controller.

Generating URLs
===============

URLs can be generated using the helper method :func:`~routes.util.url_for`, which by default in a Pylons project will be under the :data:`h` global variable or may be directly imported when used in controllers:

.. code-block:: python

    from routes import url_for

Keyword arguments indicating the controller and action to use can be 
passed directly in:

.. code-block:: python
    
    # generates /content/view/2
    h.url_for(controller='content', action='view', id=2)  

Inside templates and controllers, other variables may seem to creep into the URLs generated. This is due to `Routes memory <http://routes.groovie.org/manual.html#route-memory>`_ and can be disabled by specifying the controller with a ``/`` in front:

.. code-block:: python

    # ALWAYS generates /content/view/2
    h.url_for(controller='/content', action='view', id=2)   


.. seealso::

    `Routes manual <http://routes.groovie.org/manual.html>`_
    Full details and source code.


.. _middleware-config:

**********
Middleware
**********

Within :file:`config/middleware.py` a Pylons application is wrapped in successive layers which add functionality. The process of wrapping the Pylons application in middleware results in a structure conceptually similar to the layers in an onion.

.. image:: _static/pylons_as_onion.png
   :alt: Pylons middleware onion analogy
   :align: center

Once the middleware has been used to wrap the Pylons application, the make_app
function returns the completed app with the following structure (outermost
layer listed first):

Registry Manager
    Status Code Redirect
        Error Handler
            Cache Middleware
                Session Middleware
                    Routes Middleware
                        Pylons App (Not middleware!)

Each layer in the middleware has a common interface which underlies much of Pylons itself, called :term:`WSGI`. This basic interface declares how each layer is called, and how it must return its content and set HTTP headers.

.. note:: 
    
    There is one final piece of middleware called Cascade which is used to
    serve static content and JavaScript files during development. Before
    placing a Pylons application into production, this line should be
    commented out and the static files should be served by a webserver for
    top performance.

.. warning::

    When unsure about whether or not to change the middleware, **don't**. The
    order of the middleware is important to the proper functioning of a
    Pylons application, and shouldn't be altered unless needed.

Adding custom middleware
========================

Custom middleware should be included in the :file:`config/middleware.py` at
comment marker::

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

For example, to add a middleware component named `MyMiddleware`,
include it in :file:`config/middleware.py`::

    # The Pylons WSGI app
    app = PylonsApp()
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MyMiddleware(app)
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
The app object is simply passed as a parameter to the `MyMiddleware` middleware which in turn should return a wrapped WSGI application.

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

What is full_stack?
===================

In the Pylons ini file {:file:`development.ini` or :file:`production.ini`} this block determines if the flag full_stack is set to true or false::

    [app:main]
    use = egg:app_name
    full_stack = true

The full_stack flag determines if the ErrorHandler and StatusCodeRedirect is included as a layer in the middleware wrapping process. The only condition in which this option would be set to `false` is if multiple Pylons applications are running and will be wrapped in the appropriate middleware elsewhere.


.. _setup-config:

*****************
Application Setup
*****************



XXX: Explain how to setup app dependencies in the setup.py file to ensure
the appropriate libraries are required, explain what setup.py needs, etc.

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
* :file:`config/deployment.ini_tmpl` described in :ref:`production-config`
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
    cache_dir = config['cache.dir']

Or the current debug status like this: 

.. code-block :: python 

    debug = config['debug']

Evaluating Non-string Data in Configuration Files
-------------------------------------------------

By default, all the values in the configuration file are considered strings.
To make it easier to handle boolean values, the Paste library comes with a
function that will convert ``true`` and ``false`` to proper Python boolean
values:

.. code-block :: python
    
    from paste.deploy.converters import asbool
    
    debug = asbool(config['debug'])

This is used already in the default projects' :ref:`middleware-config` to
toggle middleware that should only be used in development mode (with
``debug``) set to true.


.. _production-config:

Production Configuration Files
==============================

To change the defaults of the configuration INI file that should be used when deploying the application, edit the :file:`config/deployment.ini_tmpl` file. This is the file that will be used as a template during deployment, so that the person handling deployment has a starting point of the minimum options the application needs set.

One of the most important options set in the deployment ini is the ``debug = true`` setting. The email options should be setup so that errors can be e-mailed to the appropriate developers or webmaster in the event of an application error.

Generating the Production Configuration
---------------------------------------

To generate the production.ini file from the projects' :file:`config/deployment.ini_tmpl` it must first be installed either as an :term:`egg` or under development mode. Assuming the name of the Pylons application is ``helloworld``, run:

.. code-block :: bash

    $ paster make-config helloworld production.ini

.. note::
    This command will also work from inside the project when its being developed.

It is the responsibility of the developer to ensure that a sensible set of default configuration values exist when the webmaster uses the ``paster make-config`` command. 

.. warning::
    **Always** make sure that the ``debug`` is set to ``false`` when deploying a Pylons application.


.. _environment-config:

***********
Environment
***********

The :file:`config/environment.py` module sets up the basic Pylons environment
variables needed to run the application. Objects that should be setup once
for the entire application should either be setup here, or in the
:file:`lib/app_globals` :meth:`__init__` method.

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

Any part of the path inside the curly braces is a variable (a `variable part`
) that will match
any text in the URL for that 'part'. A 'part' of the URL is the text between
two forward slashes. Every part of the URL must be present for the
:term:`route` to match, otherwise a 404 will be returned.

The routes above are translated by the Routes library into regular expressions
for high performance URL matching. By default, all the variable parts (except
for the special case of ``{controller}``) become a matching regular expression
of ``[^/]+`` to match anything except for a forward slash. This can be
changed easily, for example to have the ``{id}`` only match digits:

.. code-block :: python
    
    map.connect('/{controller}/{action}/{id:\d+}')

If the desired regular expression includes the ``{}``, then it should be
specified separately for the variable part. To limit the ``{id}`` to only
match at least 2-4 digits:

.. code-block :: python
    
    map.connect('/{controller}/{action}/{id}',  requirements=dict(id='\d{2,4}'))

The controller and action can also be specified as keyword arguments so that
they don't need to be included in the URL:

.. code-block :: python
    
    # Archives by 2 digit year -> /archives/08
    map.connect('/archives/{year:\d\d}', controller='articles',  action='archives')

Any variable part, or keyword argument in the ``map.connect`` statement will
be available for use in the
action used. For the route above, which resolves to the `articles`
controller:

.. code-block :: python
    
    class ArticlesController(BaseController):

        def archives(self, year):
            ...

The part of the URL that matched as the year is available by name in the
function argument.

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

.. note::
    The ``{controller}`` match is special, in that it doesn't always stop
    at the next forward slash (``/``). As the example above demonstrates,
    it is able to match controllers nested under a directory should they
    exist.

Adding a route to match ``/``
=============================

The controller and action can be specified directly in the :meth:`map.connect`
statement, as well as the raw URL to be matched:

.. code-block:: python

    map.connect('/', controller='main', action='index')

results in ``/`` being handled by the ``index`` method of the ``main``
controller.

.. note::
    By default, projects' static files (in the :file:`public/` directory) are
    served in preference to controllers. New Pylons projects include a welcome
    page (:file:`public/index.html`) that shows up at the ``/`` url. You'll
    want to remove this file before mapping a route there.

Generating URLs
===============

URLs are generated via the callable :class:`routes.util.URLGenerator`
object. Pylons provides an instance of this special object at
:data:`pylons.url`. It accepts keyword arguments indicating the desired
controller, action and additional variables defined in a route.

.. code-block:: python
    
    # generates /content/view/2
    url(controller='content', action='view', id=2)   

To generate the URL of the matched route of the current request, call
:meth:`routes.util.URLGenerator.current`:

.. code-block:: python

    # Generates /content/view/3 during a request for /content/view/3
    url.current()

:meth:`routes.util.URLGenerator.current` also accepts the same arguments as
`url()`. This uses `Routes memory
<http://routes.groovie.org/manual.html#route-memory>`_ to generate a small
change to the current URL without the need to specify all the relevant
arguments:

.. code-block:: python

    # Generates /content/view/2 during a request for /content/view/3
    url.current(id=2)

.. seealso::

    `Routes manual <http://routes.groovie.org/manual.html>`_
    Full details and source code.


.. _middleware-config:

**********
Middleware
**********

A projects WSGI stack should be setup in the :file:`config/middleware.py`
module. Ideally this file should import middleware it needs, and set it up
in the `make_app` function.

The default stack that is setup for a Pylons application is described in
detail in :ref:`wsgi-middleware`.

Default middleware stack:

.. code-block :: python

    # The Pylons WSGI app
    app = PylonsApp()
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    
    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    return app
    
Since each piece of middleware wraps the one before it, the stack needs to be
assembled in reverse order from the order in which its called. That is, the
very last middleware that wraps the WSGI Application, is the very first that
will be called by the server.

The last piece of middleware in the stack, called Cascade, is used to
serve static content files during development. For top performance,
consider disabling the Cascade middleware via setting the
``static_files = false`` in the configuration file. Then have the
webserver or a :term:`CDN` serve static files.

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
    
    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MyMiddleware(app)
    
The app object is simply passed as a parameter to the `MyMiddleware` middleware which in turn should return a wrapped WSGI application.

Care should be taken when deciding in which layer to place custom
middleware. In most cases middleware should be placed before the Pylons WSGI
application and its supporting Routes/Session/Cache middlewares, however if the
middleware should run *after* the CacheMiddleware::

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

There are two kinds of 'Application Setup' that are occasionally referenced
with regards to a project using Pylons.

* Setting up a new application
* Configuring project information and package dependencies

Setting Up a New Application
============================

To make it easier to setup a new instance of a project, such as setting up
the basic database schema, populating necessary defaults, etc. a setup
script can be created.

In a Pylons project, the setup script to be run is located in the projects'
:file:`websetup.py` file. The default script loads the projects configuration
to make it easier to write application setup steps:

.. code-block :: python
    
    import logging

    from helloworld.config.environment import load_environment

    log = logging.getLogger(__name__)

    def setup_app(command, conf, vars):
        """Place any commands to setup helloworld here"""
        load_environment(conf.global_conf, conf.local_conf)

.. note::
    If the project was configured during creation to use SQLAlchemy this file
    will include some commands to setup the database connection to make it
    easier to setup database tables.

To run the setup script using the development configuration:

.. code-block :: bash
    
    $ paster setup-app development.ini

Configuring the Package
=======================

A newly created project with Pylons is a standard Python package. As a Python
package, it has a :file:`setup.py` file that records meta-information about
the package. Most of the options in it are fairly self-explanatory, the most
important being the 'install_requires' option:

.. code-block :: python
    
    install_requires=[
        "Pylons>=0.9.7",
    ],
    
These lines indicate what packages are required for the proper functioning
of the application, and should be updated as needed. To re-parse the
:file:`setup.py` line for new dependencies:

.. code-block :: bash

    $ python setup.py develop

In addition to updating the packages as needed so that the dependency
requirements are made, this command will ensure that this package is active
in the system (without requiring the traditional
:command:`python setup.py install`).

.. seealso::
    `Declaring Dependencies <http://peak.telecommunity.com/DevCenter/setuptools#declaring-dependencies>`_

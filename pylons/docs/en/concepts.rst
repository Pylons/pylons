.. _concepts:

==================
Concepts of Pylons
==================

Understanding the basic concepts of Pylons, the flow of a request and response
through the stack and how Pylons operates makes it easier to customize when
needed, in addition to clearing up misunderstandings about why things behave
the way they do. 

This section acts as a basic introduction to the concept of
a :term:`WSGI` application, and :term:`WSGI Middleware` in addition to showing
how Pylons utilizes them to assemble a complete working web framework.

To follow along with the explanations below, create a project following the 
:ref:`getting_started` Guide.


*****************************
The 'Why' of a Pylons Project
*****************************

A new Pylons project works a little differently than in many other web
frameworks. Rather than loading the framework, which then finds a new
projects code and runs it, Pylons creates a Python package that does the
opposite. That is, when its run, it imports objects from Pylons, assembles
the WSGI Application and stack, and returns it.

If desired, a new project could be completely cleared of the Pylons imports
and run any arbitrary WSGI application instead. This is done for a greater
degree of freedom and flexibility in building a web application that works
the way the developer needs it to.

By default, the project is configured to use standard components that most
developers will need, such as sessions, template engines, caching, high
level request and response objects, and an :term:`ORM`. By having it all
setup in the project (rather than hidden away in 'framework' code), the
developer is free to tweak and customize as needed.

In this manner, Pylons has setup a project with its *opinion* of what may
be needed by the developer, but the developer is free to use the tools
needed to accomplish the projects goals. Pylons offers an unprecedented
level of customization by exposing its functionality through the project
while still maintaining a remarkable amount of simplicity by retaining a
single standard interface between core components (:term:`WSGI`).


*****************
WSGI Applications
*****************

WSGI is a basic specification known as :pep:`333`, that describes a
method for interacting with a HTTP server. This involves a way to get access
to HTTP headers from the request, and how set HTTP headers and return content
on the way back out.

A 'Hello World' WSGI Application:

.. code-block :: python
    
    def simple_app(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return ['<html><body>Hello World</body></html>']

This WSGI application does nothing but set a 200 status code for the response,
set the HTTP 'Content-type' header, and return some HTML.

The WSGI specification lays out a `set of keys that will be set in the 
environ dict <http://www.python.org/dev/peps/pep-0333/#environ-variables>`_.

The WSGI interface, that is, this method of calling a function (or method of
a class) with two arguments, and handling a response as shown above, is used
throughout Pylons as a standard interface for passing control to the next
component.

Inside a new project's :file:`config/middleware.py`, the `make_app` function is
responsible for creating a WSGI application, wrapping it in WSGI middleware
(explained below) and returning it so that it may handle requests from a
HTTP server.


.. _wsgi-middleware:

***************
WSGI Middleware
***************

Within :file:`config/middleware.py` a Pylons application is wrapped in successive layers which add functionality. The process of wrapping the Pylons application in middleware results in a structure conceptually similar to the layers in an onion.

.. image:: _static/pylons_as_onion.png
   :alt: Pylons middleware onion analogy
   :align: center

Once the middleware has been used to wrap the Pylons application, the make_app
function returns the completed app with the following structure (outermost
layer listed first):

.. code-block:: text

    Registry Manager
        Status Code Redirect
            Error Handler
                Cache Middleware
                    Session Middleware
                        Routes Middleware
                            Pylons App (WSGI Application)

WSGI middleware is used extensively in Pylons to add functionality to the
base WSGI application. In Pylons, the 'base' WSGI Application is the 
:class:`~pylons.wsgiapp.PylonsApp`. It's responsible for looking in the
`environ` dict that was passed in (from the Routes Middleware).

To see how this functionality is created, consider a small class that
looks at the `HTTP_REFERER` header to see if it's Google:

.. code-block :: python
    
    class GoogleRefMiddleware(object):
        def __init__(self, app):
            self.app = app
        
        def __call__(self, environ, start_response):
            environ['google'] = False
            if 'HTTP_REFERER' in environ:
                if environ['HTTP_REFERER'].startswith('http://google.com'):
                    environ['google'] = True
            return self.app(environ, start_response)

This is considered WSGI Middleware as it still can be called and returns
like a WSGI Application, however, it's adding something to environ, and then
calls a WSGI Application that it is initialized with. That's how the layers
are built up in the `WSGI Stack` that is configured for a new Pylons project.

Some of the layers, like the Session, Routes, and Cache middleware, only add
objects to the `environ` dict, or add HTTP headers to the response (the Session middleware for example adds the session cookie header). Others, such
as the Status Code Redirect, and the Error Handler may fully intercept the
request entirely, and change how it's responded to.


*******************
Controller Dispatch
*******************

When the request passes down the middleware, the incoming URL gets parsed in
the RoutesMiddleware, and if it matches a URL (See :ref:`url-config`), the
information about the controller that should be called is put into the `environ` dict for use by :class:`~pylons.wsgiapp.PylonsApp`.

The :class:`~pylons.wsgiapp.PylonsApp` then attempts to find a controller in the :file:`controllers`
directory that matches the name of the controller, and searches for a class
inside it by a similar scheme (controller name + 'Controller', ie,
HelloController). Upon finding a controller, its then called like any other
WSGI application using the same WSGI interface that
:class:`~pylons.wsgiapp.PylonsApp` was called with.

.. versionadded:: 1.0
    Controller name can also be a dotted path to the module / callable that
    should be imported and called. For example, to use a controller named
    'Foo' that is in the 'bar.controllers' package, the controller name
    would be `bar.controllers:Foo`.
 
This is why the BaseController that resides in a project's
:file:`lib/base.py` module inherits from
:class:`~pylons.controllers.core.WSGIController` and has a `__call__`
method that takes the `environ` and `start_response`. The
:class:`~pylons.controllers.core.WSGIController` locates a method in the
class that corresponds to the `action` that Routes found, calls it, and 
returns the response completing the request.


******
Paster
******

Running the :command:`paster` command all by itself will
show the sets of commands it accepts:

.. code-block :: bash
    
    $ paster
    Usage: paster [paster_options] COMMAND [command_options]

    Options:
      --version         show program's version number and exit
      --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
                        specs; will also require() the Egg)
      -h, --help        Show this help message

    Commands:
      create          Create the file layout for a Python distribution
      grep            Search project for symbol
      help            Display help
      make-config     Install a package and create a fresh config file/directory
      points          Show information about entry points
      post            Run a request for the described application
      request         Run a request for the described application
      serve           Serve the described application
      setup-app       Setup an application, given a config file

    pylons:
      controller      Create a Controller and accompanying functional test
      restcontroller  Create a REST Controller and accompanying functional test
      shell           Open an interactive shell with the Pylons app loaded

If :command:`paster` is run inside of a Pylons project, this should be the
output that will be printed. The last section, `pylons` will be absent if
it is not run inside a Pylons project. This is due to a dynamic plugin
system the :command:`paster` script uses, to determine what sets of
commands should be made available.

Inside a Pylons project, there is a directory ending in `.egg-info`, that has
a :file:`paster_plugins.txt` file in it. This file is looked for and read by
the :command:`paster` script, to determine what other packages should be
searched dynamically for commands. Pylons makes several commands available
for use in a Pylons project, as shown above.


***********************
Loading the Application
***********************

Running (and thus loading) an application is done using the :command:`paster`
command:

.. code-block :: bash
    
    $ paster serve development.ini

This instructs the paster script to go into a 'serve' mode. It will attempt
to load both a server and a WSGI application that should be served, by
parsing the configuration file specified. It looks for a `[server]` block to
determine what server to use, and an `[app]` block for what WSGI application
should be used.

The basic egg block in the :file:`development.ini` for a `helloworld` project:


.. code-block :: ini
    
    [app:main]
    use = egg:helloworld

That will tell paster that it should load the helloworld :term:`egg` to locate
a WSGI application. A new Pylons application includes a line in the
:file:`setup.py` that indicates what function should be called to make the
WSGI application:

.. code-block :: python
    
    entry_points="""
    [paste.app_factory]
    main = helloworld.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,

Here, the `make_app` function is specified as the `main` WSGI application that
Paste (the package that :command:`paster` comes from) should use.

The `make_app` function from the project is then called, and the server (by
default, a HTTP server) runs the WSGI application.

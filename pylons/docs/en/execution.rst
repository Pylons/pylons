Pylons Execution Analysis
%%%%%%%%%%%%%%%%%%%%%%%%%

*By Mike Orr and Alfredo Deza*

This chapter shows how Pylons calls your application, and how Pylons interacts
with Paste, Routes, Mako, and its other dependencies.  We'll create
a simple application and then analyze the Python code executed starting from
the moment we run the "paster serve" command.

**Abbreviations:** **$APP** is your top-level application directory. 
**$SP** is the site-packages directory where Pylons is installed.
**$BIN** is the location of ``paster`` and other executables. $SP paths are
shown in pip style ($SP/pylons) rather than easy_install style
($SP/Pylons-VERSION.egg/pylons).

The sample application
========================

1. Create an application called "Analysis" with a controller called "main"::

    $ paster create -t pylons Analysis
    $ cd Analysis
    $ paster controller main

   Press Enter at all question prompts.

2. Edit **analysis/controllers/main.py** to look like this::

        from analysis.lib.base import BaseController

        class MainController(BaseController):

            def index(self):
                return '<h1>Welcome to the Analysis Demo</h1>Here is a <a href="/page2">link</a>.'

            def page2(self):
                return 'Thank you for using the Analysis Demo. <a href="/">Home</a>'
                
   There are two shortcuts here which you would not use in a normal
   application. One, we're returning incomplete HTML documents. Two, we've
   hardcoded the URLs to make the analysis easier to follow, rather than using
   the ``url`` object.

3. Now edit **analysis/config/routing.py**.  Add these lines after "CUSTOM
   ROUTES HERE" (line 21)::

    map.connect("home", "/", controller="main", action="index")
    map.connect("page2", "/page2", controller="main", action="page2")

4. Delete the file **analysis/public/index.html**.

5. Now run the server.  (Press ctrl-C to quit it.) ::

    $ paster serve development.ini
    Starting server in PID 7341.
    serving on http://127.0.0.1:5000


Pylons' dependencies
====================

Pylons 1.0 has the following direct and indirect dependencies, which will be
found in your site-packages directory ($SP):

* Beaker 1.5.4
* decorator 3.2.0
* FormEncode 1.2.2
* Mako 0.3.4
* MarkupSafe 0.9.3
* Nose 0.11.4
* Paste 1.7.3.1
* PasteDeploy 1.3.3
* PasteScript 1.7.3
* Routes 1.12.3
* simplejson 2.0.9 (if Python < 2.6)
* Tempita 0.4
* WebError 0.10.2
* WebHelpers 1.2
* WebOb 0.9.8
* Webtest 1.2.1

These are the current versions as of August 29, 2010. Your installation may have
slightly newer or older versions.

The analysis
============

Startup (PasteScript)
---------------------

When you run ``paster serve development.ini``, it runs the "$BIN/paster" program.
This is a platform-specific stub created by ``pip`` or ``easy_install``.  It
does this::

    __requires__ = 'PasteScript==1.7.3'
    import sys
    from pkg_resources import load_entry_point

    sys.exit(
       load_entry_point('PasteScript==1.7.3', 'console_scripts', 'paster')()
    )

This says to load a Python object "paster" located in an egg "PasteScript",
version 1.7.3, under the entry point group ``[console_scripts]``.  

To explain what this means we have to get into Setuptools. Setuptools is
Python's de facto package manager, and was installed as part of your virtualenv
or Pylons installation. (If you're using Distribute 0.6, an alternative
package manager, it works the same way.) ``load_entry_point`` is a function
that looks up a Python object via entry point and returns it.

So what's an entry point? It's an alias for a Python object. Here's the entry
point itself::

        [console_scripts]
        paster=paste.script.command:run

This is from $SP/PasteScript-VERSION.egg-info/entry_points.txt.
(If you used easy_install rather than pip, the path would be slightly
different: $APP/PasteScript-VERSION.egg/EGG-INFO/entry_points.txt.)

"console_scripts" is the entry point group. "paster" is the
entry point. The right side of the value tells which module to import
(``paste.script.command``) and which object in it to return (the ``run``
function). (To create an entry point, define it in your package's setup.py. Pip
or easy_install will create the egg_info metadata from that. If you modify a
package's entry points, you must reinstall the package to update the egg_info.)

The most common use case for entry points is for plugins. So Nose for instance
defines an entry point group by which it will look for plugins. Any other
package can provide plugins for Nose by defining entry points in that group.
Paster uses plugins extensively, as we'll soon see.

So to make a long story short, "paster serve" calls this ``run`` function. I
inserted print statements into ``paste.script.command`` to figure out what it
does. Here's a simplified description:

1. The ``run()`` function parses the command-line options into a subcommand 
   ``"serve"`` with arguments ``["development.ini"]``.

2. It calls ``get_commands()``, which loads Paster commands from plugins
   located at various entry points.  (You can add custom commands with the
   "--plugin" command-line argument.)  Paste's standard commands are listed in
   the same entry_points.txt file we saw above::

        [paste.global_paster_command]
        serve=paste.script.serve:ServeCommand [Config]
        #... other commands like "make-config", "setup-app", etc ...

3. It calls ``invoke()``, which essentially does
   ``paste.script.serve.ServeCommand(["development.ini"]).run()``. This in turn
   calls ``ServeCommand.command()``, which handles daemonizing and other
   top-level stuff.  Since our command line is short, there's no top-level
   stuff to do. It creates 'server' and 'app' objects based on the
   configuration file, and calls ``server(app)``.

Loading the server and the application (PasteDeploy)
----------------------------------------------------

This all happens during step 3 of the application startup. We need to find and
instantiate the WSGI application and server based on the configuration file.
The application is our Analysis application.  The server is Paste's built-in
multithreaded HTTP server.  A simplified version of the code is::

    # Inside paste.script.serve module, ServeCommand.command() method.
    from paste.deploy.loadwsgi import loadapp, loadserver
    server = self.loadserver(server_spec, name=server_name,
                                     relative_to=base, global_conf=vars)
    app = self.loadapp(app_spec, name=app_name,
                      relative_to=base, global_conf=vars)

``loadserver()`` and ``loadapp()`` are defined in module
``paste.deploy.loadwsgi``. The code here is complex, so we'll just look at its
general behavior. Both functions see the "config:" URI and read our config
file. Since there is no server name or app name they both default to "main".
Therefore loadserver() looks for a "\[server:main]" section in the config file,
and loadapp()` looks for "\[app:main]". Here's what they find in
"development.ini"::

    [server:main]
    use = egg:Paste#http
    host = 127.0.0.1
    port = 5000

    [app:main]
    use = egg:Analysis
    full_stack = true
    static_files = true
    ...

The "use =" line in each section tells which object to load. The other lines
are configuration parameters for that object, or for plugins that object is
expected to load.  We can also put custom parameters in \[app:main] for our
application to read directly.


Server loading
++++++++++++++

1. ``loadserver()``'s args are ``uri="config:development.ini", name=None,
   relative_to="$APP"``.

2. A "config:" URI means to read a config file.

3. A server name was not specified so it defaults to "main". So loadserver()
   looks for a section "\[server:main]". The "server" part comes from the
   loadwsgi._Server.config_prefixes class attribute in
   $SP/paste/deploy/loadwsgi.py).

4. "use = egg:Paste#http" says to load an egg called "Paste".

5. loadwsgi._Server.egg_protocols lists two protocols it supports:
   "server_factory" and "server_runner".

6. "paste.server_runner" is an entry point group in the "Paste" egg, and it has
   an entry point "http". The relevant lines in
   $SP/Paste\*.egg_info/entry_points.txt are::

        [paste.server_runner]
        http = paste.httpserver:server_runner

7. There's a server_runner() function in the paste.httpserver module
   ($SP/paste/httpserver.py).

We'll stop here for a moment and look at how the application is loaded.

Application loading
+++++++++++++++++++

1. loadapp() looks for a section "\[app:main]" in the config file. The "app"
   part comes from the loadwsgi._App.config_prefixes class attribute (in
   $SP/paste/deploy/loadwsgi.py).

2. "use = egg:Analysis" says to find an egg called "Analysis".

3. loadwsgi._App.egg_protocols lists "paste.app_factory" as one of the
   protocols it supports.

4. "paste.app_factory" is also an entry point group in the egg, as seen in
   $APP/Analysis.egg-info/entry_points.txt::

        [paste.app_factory]
        main = analysis.config.middleware:make_app

5. The line "main = analysis.config.middleware:make_app" means to 
   look for a ``make_app()`` object in the ``analysis`` package. 
   This is a function imported from ``analysis.config.middleware`` 
   ($APP/analysis/config/middleware.py).


Instantiating the application (Analysis)
----------------------------------------

Here's a closer look at our application's ``make_app`` function::

    # In $APP/analysis/config/middleware.py
    def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
        config = load_environment(global_conf, app_conf)
        app = PylonsApp(config=config)
        app = SomeMiddleware(app, ...)   # Repeated for several middlewares.
        app.config = config
        return app

This sets up the Pylons environment (next subsection), creates the application
object (following subsection), wraps it in several layers of middleware (listed
in "Anatomy of a Request" below), and returns the complete application object.

The \[DEFAULT] section of the config file is passed as dict ``global_conf``.
The \[app:main] section is passed as keyword arguments into dict ``app_conf``.

``full_stack`` defaults to True because we're running the application
standalone.  If we were embedding this application as a WSGI component of some
larger application, we'd set ``full_stack`` to False to disable some of the
middleware.  

``static_files=True`` means to serve static files from our public
directory ($APP/analysis/public). Advanced users can arrange for Apache to
serve the static files itself, and put "static_files = false"
in their configuration file to gain a bit of efficiency.

load_environment & pylons.config
++++++++++++++++++++++++++++++++

Before we begin, remember that ``pylons.config``, ``pylons.app_globals``,
``pylons.request``, ``pylons.response``, ``pylons.session``, ``pylons.url``,
and ``pylons.cache`` are special globals that change value depending on the
current request. The objects are proxies which maintain a thread-local stack of
real values.  Pylons pushes the actual values onto them at the beginning of a
request, and pops them off at the end. (Some of them it also pushes at other
times so they can be used outside of requests.) The proxies delegate attribute
access and key access to the topmost actual object on the stack. (You can also
call ``myproxy._current_obj()`` to get the actual object itself.)  The proxy
code is in ``paste.registry.StackedObjectProxy``, so these are called
"StackedObjectProxies", or "SOPs" for short.

The first thing ``analysis.config.middleware.make_app()`` does is call
``analysis.config.environment.load_environment()``::

    def load_environment(global_conf, app_conf):
        config = PylonsConfig()
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths = dict(root=root,
                     controllers=os.path.join(root, 'controllers'),
                     static_files=os.path.join(root, 'public'),
                     templates=[os.path.join(root, 'templates')])

        # Initialize config with the basic options
        config.init_app(global_conf, app_conf, package='analysis',
                        paths=paths)
        config['routes.map'] = make_map(config)
        config['pylons.app_globals'] = app_globals.Globals(config)
        config['pylons.h'] = analysis.lib.helpers

        # Setup cache object as early as possible
        import pylons
        pylons.cache._push_object(config['pylons.app_globals'].cache)

        # Create the Mako TemplateLookup, with the default auto-escaping
        config['pylons.app_globals'].mako_lookup = TemplateLookup(
            directories=paths['templates'],
            error_handler=handle_mako_error,
            module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
            input_encoding='utf-8', default_filters=['escape'],
            imports=['from webhelpers.html import escape'])

        # CONFIGURATION OPTIONS HERE (note: all config options will override
        # any Pylons config options)

        return config

``config`` is the Pylons configuration object, which will later be pushed onto
``pylons.config``. It's an instance of ``pylons.configuration.PylonsConfig``, a
dict subclass. ``config.init_app()`` initializes the dict's keys.  It sets the
keys to a merger of app_conf and global_conf (with app_conf overriding). It
also adds "app_conf" and "global_conf" keys so you can access the original
app_conf and global_conf if desired. It also adds several Pylons-specific keys.

``config["routes.map"]`` is the Routes map defined in
``analysis.config.routing.make_map()``. 

``config["pylons.app_globals"]`` is the application's globals object, which
will later be pushed onto ``pylons.app_globals``.  It's an instance of
``analysis.lib.app_globals.Globals``.

``config["pylons.h"]`` is the helpers module, ``analysis.lib.helpers``. Pylons
will assign it to ``h`` in the templates' namespace.

The "cache" lines push ``pylons.app_globals.cache`` onto ``pylons.cache`` for
backward compatibility.  This gives a preview of how StackedObjectProxies work.

The Mako stanza creates a TemplateLookup, which ``render()`` will use to find
templates. The object is put on ``app_globals``.

If you've used older versions of Pylons, you'll notice a couple differences in
1.0.  The ``config`` object is created as a local variable and returned, and
it's passed explicitly to the route map factory and globals factory. Previous
versions pushed it onto ``pylons.config`` immediately and used it from there.
This was changed to make it easier to nest Pylons applications inside other
Pylons applications. 

The other difference is that Buffet is gone, and along with it the
``template_engine`` argument and template config options. Pylons 1.0 gets out
of the business of initializing template engines.  You use one of the standard
render functions such as ``render_mako`` or write your own, and define any
attributes in ``app_globals`` that your render function depends on.


PylonsApp
+++++++++

The second line of ``make_app()`` creates a Pylons application object
based on your configuration.  Again the ``config`` object is passed around
explicitly, unlike older versions of Pylons. A Pylons application is an
instance of ``pylons.wsgiapp.PylonsApp`` instance. (Older versions of Pylons
had a ``PylonsBaseWSGIApp`` superclass, but that has been merged into
``PylonsApp``.)

Middleware
++++++++++

``make_app()`` then wraps the application (the ``app`` variable) in several
layers of middleware. Each middleware provides an optional add-on service. 

================== ============================ ===============================
Middleware         Service                      Effect if disabled
================== ============================ ===============================
RoutesMiddleware   Use Routes to manage URLs.   Routes and ``pylons.url`` won't
                                                work.
SessionMiddleware  HTTP sessions using Beaker,  ``pylons.session`` won't work.
                   with flexible persistence
                   backends (disk, memached,
                   database).
ErrorHandler       Display interactive          Paste will catch exceptions and 
                   traceback if an exception    convert them to Internal Server
                   occurs. In production mode,  Error.
                   email the traceback to the
                   site admin.
StatusCodeRedirect If an HTTP error occurs,     If an HTTP error occurs, 
                   make a subrequest to display display a plain white HTML page
                   a fancy styled HTML error    with the error message.
                   page.
RegistryManager    Handles the special globals  The special globals won't work. 
                   (``pylons.request``, etc).   There are other ways to access
                                                the objects without going
                                                through the special globals.
StaticURLParser    Serve the static files       The static files won't be 
                   in the application's         found. Presumably you've
                   public directory.            configured Apache to serve them
                                                directly.
Cascade            Call several sub-middlewares No cascading through
                   in order, and use the first  alternative apps.
                   one that doesn't return
                   "404 Not Found". Used in
                   conjunction with 
                   StaticURLParser.
================== ============================ ===============================

At the end of the function, ``app.config`` is set to the ``config`` object, so
that any part of the application can access the config without going through
the special global.

Anatomy of a request
--------------------

Let's say you're running the demo and click the "link" link on the home page.
The browser sends a request for "http://localhost:5000/page2".  In my Firefox
the HTTP request headers are::

    GET /page2 
    Host: 127.0.0.1:5000
    User-Agent: Mozilla/5.0 ...
    Accept: text/html,...
    Accept-Language: en-us,en;q=0.5
    Accept-Encoding: gzip,deflate
    Accept-Charset: ISO-8859-1,utf-8;q=0.7*;q=0.7
    Keep-Alive: 300
    Connection: keep-alive
    Referer: http://127.0.0.1/5000/
    Cache-Control   max-age=0

The response is::

    HTTP/1.x 200 OK
    Server: PasteWSGIServer/0.5 Python/2.6.4
    Date: Sun, 06 Dec 2009 14:06:05 GMT
    Content-Type: text/html; charset=utf-8
    Pragma:  no-cache
    Cache-Control:   no-cache
    Content-Length:  59

    Thank you for using the Analysis Demo.  <a href="/">Home</a>

Here's the processing sequence:

1. ``server(app)`` is still running, called by ``ServeCommand.command()`` in
   $SP/paste/script/serve.py.

2. ``server`` is actually ``paste.httpserver.server_runner()`` in
   $SP/paste/httpserver. The only keyword args are 'host' and
   'port' extracted from the config file.  ``server_runner`` de-stringifies
   the arguments and calls ``serve(wsgi_app, **kwargs)`` (same module).  

3. ``serve()``'s 'use_threadpool' arg defaults to True, so it creates a
   ``WSGIThreadPoolServer`` instance called (``server``) with the following
   inheritance::

        SocketServer.BaseServer     # In SocketServer.py in Python stdlib.
        BaseHTTPServer.HTTPServer  # In BaseHTTPServer.py in Python stdlib.
        paste.httpserver.SecureHTTPServer  # Adds SSL (HTTPS).
        paste.httpserver.WSGIServerBase    # Adds WSGI.
        paste.httpserver.WSGIThreadPoolServer
            multiple inheritance: ThreadPoolMixIn <= ThreadPool

    Note that SecureHTTPServer overrides the implementation of Python's
    SocketServer.TCPServer

4. It calls ``server.serve_forever()``, implemented by the ``ThreadPoolMixIn``
   superclass.  This calls ``self.handle_request()`` in a loop until
   ``self.running`` becomes false.  That initiates this call stack::

        # In paste.httpserver.serve(), calling 'server.serve_forever()'
        ThreadPoolMixIn.serve_forever()  # Defined in paste.httpserver.
        -> TCPServer.handle_request()    # Called for every request.
        -> WSGIServerBase.get_request()
        -> SecureHTTPServer.get_request()
        -> self.socket.accept()          # Defined in stdlib socket module.

   ``self.socket.accept()`` blocks, waiting for the next request.

5. The request arrives and ``self.socket.accept()`` returns a new socket for
   the connection. ``TCPServer.handle_request()`` continues. It calls
   ``ThreadPoolMixIn.process_request()``, which puts the request in a thread
   queue::

        self.thread_pooladd.add_task(
            lambda: self.process_request_in_thread(request, client_address))
            # 'request' is the connection socket.

   The thread pool is defined in the ``ThreadPool`` class. It spawns a number
   of threads which each wait on the queue for a callable to run. In this case
   the callable will be a complete Web transaction including sending the HTML
   page to the client. Each thread will repeatedly process transactions from
   the queue until they receive a sentinel value ordering them to die.

   The main thread goes back to listening for other requests, so we're no
   longer interested in it.

6. **Thread #2** pulls the lambda out of the queue and calls it::

        lambda
        -> ThreadPoolMixIn.process_request_in_thread()
        -> BaseServer.finish_request()
        -> self.RequestHandlerClass(request, client_address, self)  # Instantiates this.
           The class instantiated is paste.httpserver.WSGIHandler; i.e., the 'handler' variable in serve().

7. The newly-created request handler takes over::

        SocketServer.BaseRequestHandler.__init__(request, client_address, server)
        -> WSGIHandler.handle()
        -> BaseHTTPRequestHandler.handle()  # In stdlib BaseHTTPServer.py
           Handles requests in a loop until self.close_connection is true.  (For HTTP keepalive?)
        -> WSGIHandler.handle_one_request()
           Reads the command from the socket.  The command is
           "GET /page2 HTTP/1.1" plus the HTTP headers above.
           BaseHTTPRequestHandler.parse_request() parses this into attributes
           .command, .path, .request_version, and .headers.
        -> WSGIHandlerMixin.wsgi_execute().
        -> WSGIHandlerMixin.wsgi_setup()
           Creates the .wsgi_environ dict.

   The WSGI environment dict is described in PEP 333, the WSGI specification.
   It contains various keys specifying the URL to fetch, query parameters,
   server info, etc. All keys required by the CGI specification are present,
   as are other keys specific to WSGI or to paricular middleware. The
   application will calculate a response based on the dict. The application is
   wrapped in layers of middleware -- nested function calls -- which modify
   the dict on the way in and modify the response on the way out.

8. The request handler, still in ``WSGIHandlerMixin.wsgi_execute()``, calls the
   application thus::

        result = self.server.wsgi_application(self.wsgi_environ,
                                            self.wsgi_start_response)

   ``wsgi_start_response`` is a callable mandated by the WSGI spec. The
   application will call it to specify the HTTP headers. The return value is
   an iteration of strings, which when concatenated form the HTML document to
   send to the browser. Other MIME types are handled analagously.

9. The application, as we remember, was returned by
   ``analysis.config.middleware.make_app()``. It's wrapped in several layers
   of middleware, so calling it will execute the middleware in reverse order
   of how they're listed in $APP/analysis/config/middleware.py and
   $SP/pylons/wsgiapp.py:

        * ``Cascade`` (defined in $SP/paste/cascade.py) lists a 
          series of applications which will be tried in order (Skipped if static_files is set to False):

                1. ``StaticURLParser`` (defined in 
                   $SP/paste/urlparser) looks for a file URL
                   under $APP/analysis/public that matches the URL.  The demo
                   has no static files.

                2. If that fails the cascader tries your application.  
                   But first there are other middleware to go through...

        * ``RegistryManager`` (defined in $SP/paste/registry.py) 
          makes Pylons special globals both thread-local and middleware-local.
          This includes **app_globals**, **cache**, **request**, **response**,
          **session**, **tmpl_context**, **url**, and any other
          ``StackedObjectProxy`` listed in $SP/pylons/__init__.py.  (**h** is
          a module so it doesn't need a proxy.)

        * ``StatusCodeRedirect`` (defined in $SP/pylons/middleware.py)
          intercepts any HTTP error status returned by the application (e.g.,
          "Page Not Found", "Internal Server Error") and sends another request
          to the application to get the appropriate error page to display
          instead. (Skipped if ``full_stack`` argument was false.)

        * ``ErrorHandler`` (defined in $SP/pylons/middleware.py)
          sends an interactive traceback to the browser if the app raises an
          exception, if "debug" is true in the config file.  Otherwise it
          attempts to email the traceback to the site administrator, and
          substitutes a generic Internal Server Error for the response.
          (Skipped if ``full_stack`` argument was false.

        * User-defined middleware goes here.

        * ``SessionMiddleware`` (wsgiapp.py) adds `Beaker`_
          session support (the ``pylons.session`` object).  (Skipped if the
          WSGI environment has a key 'session' -- it doesn't in this demo.)

        * ``RoutesMiddleware`` (wsgiapp.py) compares the request URI against the
          routing rules in $APP/analysis/config/routing.py and sets
          'wsgi.routing_args' to the routing match dict (useful) and
          'routes.route' to the Route (probably not useful).  Pylons 1.0 apps
          have a ``singleton=False`` argument that suppresses initializing the
          deprecated ``url_for()`` function. Routes now puts a URL
          generator in the WSGI environment, which Pylons aliases to
          ``pylons.url``.

        * The innermost middleware calls the PylonsApp instance it was 
          initialized with.

    Note: CacheMiddleware is no longer used in Pylons 1.0. Instead,
    ``app_globals`` creates the cache as an attribute, and a line in
    environment.py aliases ``pylons.cache`` to it.

10. Surprise! PylonsApp is itself middleware. Its .\_\_call\_\_() method does::

        self.setup_app_env(environ, start_response)
        controller = self.resolve(environ, start_response)
        response = self.dispatch(controller, environ, start_response)
        return response

    ``.setup_app_env()`` registers all those special globals.

    ``.resolve()`` calculates the controller class based on the route chosen by
    the RoutesMiddleware, and returns the controller class.

    ``.dispatch`` instantiates the controller class and calls in the WSGI
    manner.  If the controller does not exist (``.resolve()`` returned None),
    raise an Exception that tells you what controller did not have any 
    content.

    This method also handles the special URL "/_test_vars", which is enabled
    if the application is running under a Nose test. This URL initializes
    Pylons' special globals, for tests that have to access them before making
    a regular request.

11. ``analysis.controllers.main.MainController`` does not have a
    ``.\_\_call\_\_()`` method, so control falls to its parent,
    ``analysis.lib.base.BaseController``.  This trivially calls the
    grandparent, ``pylons.controllers.WSGIController``. It calls the action
    method ``MainController.page2()``. The action method may have any number of
    positional arguments as long as they correspond to variables in the routing
    match dict.  (GET/POST variables are in the **request.params** dict.)  If
    the method has a ``\*\*kwargs`` argument, all other match variables are put
    there.  Any variables passed to the action method are also put on the
    **tmpl_context** object as attributes. If an action method name
    starts with "\_", it's private and HTTPNotFound is raised.

12. If the controller has .\_\_before\_\_() and/or .\_\_after\_\_() methods,
    they are called before and after the action, respectively. These can
    perform authorization, lock OS resources, etc. These methods can have
    arguments in the same manner as the action method.  However, if the code is
    used by all controllers, most Pylons programmers prefer to it in the base
    controller's ``.\_\_call\_\_`` method instead.

13. The action method returns a string, unicode, Response object, or is a
    generator of strings. In this trivial case it returns a string. A typical
    Pylons action would set some *tmpl_context* attributes and 'return
    render('/some/template.html")' . In either case the global *response*
    object's body would be set to the string.

14. ``WSGIController.\_\_call\_\_()`` continues, converting the Response object
    to an appropriate WSGI return value. (First it calls the start_response
    callback to specify the HTTP headers, then it returns an iteration of
    strings.  The Response object converts unicode to utf-8 encoded strings, or
    whatever encoding you've specified in the config file.)

15. The stack of middleware calls unwinds, each modifying the return value and
    headers if it desires.  

16. The server receives the final return value. (We're way back in
    ``paste.httpserver.WSGIHandlerMixin.wsgi_execute()`` now.) The outermost
    middleware has called back to ``server.start_response()``, which has saved
    the status and HTTP headers in ``.wsgi_curr_headers``. ``.wsgi_execute()``
    then iterates the application's return value, calling
    ``.wsgi_write_chunk(chunk)`` for each encoded string yielded.
    ``.wsgi_write_chunk('')`` formats the status and HTTP headers and sends them
    on the socket if they haven't been sent yet, then sends the chunk. The
    convoluted header behavior here is mandated by the WSGI spec.

17. Control returns to ``BaseHTTPRequestHandler.handle()``.
    ``.close_connection`` is true so this method returns. The call stack
    continues unwinding all the way to
    ``paste.httpserver.ThreadPoolMixIn.process_request_in_thread()``. This
    tries to finish the request first and then close it unless it finds errors in it to end raising an Exception.

18. The request lambda finishes and control returns to
    ``ThreadPool.worker_thread_callback()``. It waits for another request in
    the thread queue. If the next item in the queue is the shutdown sentinel
    value, thread #2 dies.

Thus endeth our request's long journey, and this analysis is finished too.

.. _beaker:  http://beaker.groovie.org/

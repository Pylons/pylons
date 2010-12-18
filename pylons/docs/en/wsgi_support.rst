.. _wsgi_support:

============
WSGI support
============

The Web Server Gateway Interface `defined in PEP 333 <http://www.python.org/dev/peps/pep-0333/>`_ is a standard interface between web servers and Python web applications or frameworks, to promote web application portability across a variety of web servers. 

Pylons supports the Web Server Gateway Interface (or WSGI for short, pronounced "wizgy") throughout its stack. This is important for developers because it means that as well coming with all the features you would expect of a modern web framework, Pylons is also extremely flexible. With the WSGI it is possible to change any part of the Pylons stack to add new functionality or modify a request or a response without having to take apart the whole framework. 

Paste and WSGI 
-------------- 

Most of Pylons' WSGI capability comes from its close integration with Paste. Paste provides all the tools and middleware necessary to deploy WSGI applications. It can be thought of as a low-level WSGI framework designed for other web frameworks to build upon. Pylons is an example of a framework which makes full use of the possibilities of Paste. 

If you want to, you can get the WSGI application object from your Pylons configuration file like this: 

.. code-block:: python 

    from paste.deploy import loadapp 
    wsgi_app = loadapp('config:/path/to/config.ini') 

You can then serve the file using a WSGI server. Here is an example using the WSGI Reference Implementation included with Python 2.5: 

.. code-block:: python 

    from paste.deploy import loadapp 
    wsgi_app = loadapp('config:/path/to/config.ini') 

    from wsgiref import simple_server 
    httpd = simple_server.WSGIServer(('',8000), simple_server.WSGIRequestHandler) 
    httpd.set_app(wsgi_app) 
    httpd.serve_forever() 

The ``paster serve`` command you will be used to using during the development of Pylons projects combines these two steps of creating a WSGI app from the config file and serving the resulting file to give the illusion that it is serving the config file directly. 

Because the resulting Pylons application is a WSGI application it means you can do the same things with it that you can do with any WSGI application. For example add a middleware chain to it or serve it via FastCGI/SCGI/CGI/mod_python/AJP or standalone. 

You can also configure extra WSGI middleware, applications and more directly using the configuration file. The various options are described in the `Paste Deploy Documentation <http://pythonpaste.org/deploy/>`_ so we won't repeat them here. 

Using a WSGI Application as a Pylons 0.9 Controller 
--------------------------------------------------- 

In Pylons 0.9 controllers are derived from ``pylons.controllers.WSGIController`` and are also valid WSGI applications. Unless your controller is derived from the legacy ``pylons.controllers.Controller`` class it is also assumed to be a WSGI application. This means that you don't actually need to use a Pylons controller class in your controller, any WSGI application will work as long as you give it the same name. 

For example, if you added a ``hello`` controller by executing ``paster controller hello``, you could modify it to look like this: 

.. code-block:: python 

    def HelloController(environ, start_response): 
        start_response('200 OK', [('Content-Type','text/html')]) 
        return ['Hello World!'] 

or use ``yield`` statements like this: 

.. code-block:: python 

    def HelloController(environ, start_response): 
        start_response('200 OK', [('Content-Type','text/html')]) 
        yield 'Hello ' 
        yield 'World!' 

or use the standard Pylons ``Response`` object which is a valid WSGI response which takes care of calling ``start_response()`` for you: 

.. code-block:: python 

    def HelloController(environ, start_response): 
        return Response('Hello World!') 

and you could use the ``render()`` and ``render_response()`` objects exactly like you would in a normal controller action. 

As well as writing your WSGI application as a function you could write it as a class: 

.. code-block:: python 

    class HelloController: 

        def __call__(self, environ, start_response): 
            start_response('200 OK', [('Content-Type','text/html')]) 
            return ['Hello World!'] 

All the standard Pylons middleware defined in ``config/middleware.py`` is still available. 

Running a WSGI Application From Within a Controller 
--------------------------------------------------- 

There may be occasions where you don't want to replace your entire controller with a WSGI application but simply want to run a WSGI application from with a controller action. If your project was called ``test`` and you had a WSGI application called ``wsgi_app`` you could even do this: 

.. code-block:: python 

    from test.lib.base import * 

    def wsgi_app(environ, start_response): 
        start_response('200 OK',[('Content-type','text/html')]) 
        return ['<html>\n<body>\nHello World!\n</body>\n</html>'] 

    class HelloController(BaseController): 
        def index(self): 
            return wsgi_app(request.environ, self.start_response) 

Configuring Middleware Within a Pylons Application 
-------------------------------------------------- 

A Pylons application middleware stack is directly exposed in the project's ``config/middleware.py`` file. This means that you can add and remove pieces from the stack as you choose. 

.. Warning:: If you remove any of the default middleware you are likely to find that various parts of Pylons stop working! 

As an example, if you wanted to add middleware that added a new key to the environ dictionary you might do this: 

.. code-block:: python 

    # YOUR MIDDLEWARE 
    # Put your own middleware here, so that any problems are caught by the error 
    # handling middleware underneath 

    class KeyAdder: 
    def __init__(self, app, key, value): 
        self.app = app 
        if '.' not in key: 
            raise Exception("WSGI environ keys must contain a '.' character") 
        self.key = key 
        self.value = value 

    def __call__(self, environ, start_response): 
        environ[self.key] = self.value 
        return self.app(environ, start_response) 

    app = KeyAdder(app, 'test.hello', 'Hello World') 

Then in your controller you could write: 

.. code-block:: python 

    return Response(request.environ['test.hello']) 

and you would see your ``Hello World!`` message. 

Of course, this isn't a particularly useful thing to do. Middleware classes can do one of four things or a combination of them: 

* Change the environ dictionary 
* Change the status 
* Change the HTTP headers 
* Change the response body of the application 

With the ability to do these things as a middleware you can create authentication code, error handling middleware and more but the great thing about WSGI is that someone probably already has so you can consult the `wsgi.org middleware list <http://wsgi.org/wsgi/Middleware_and_Utilities>`_ or have a look at the `Paste project <http://pythonpaste.org>`_ and reuse an exisiting piece of middleware. 

The Cascade 
----------- 

Towards the end of the middleware stack in your project's ``config/middleware.py`` file you will find a special piece of middleware called the cascade: 

.. code-block:: python 

    app = Cascade([static_app, javascripts_app, app]) 

Passed a list of applications, ``Cascade`` will try each of them in turn. If one returns a 404 status code then the next application is tried until one of the applications returns a code other than ``404`` in which case its response is returned. If all applications fail, then the last application's failure response is used. 

The three WSGI applications in the cascade serve files from your project's ``public`` directory first then if nothing matches, the WebHelpers module JavaScripts are searched and finally if no JavaScripts are found your Pylons app is tried. This is why the ``public/index.html`` file is served before your controller is executed and why you can put ``/javascripts/`` into your HTML and the files will be found. 

You are free to change the order of the cascade or add extra WSGI applications to it before ``app`` so that other locations are checked before your Pylons application is executed. 

Useful Resources 
---------------- 

Whilst other frameworks have put WSGI adapters at the end of their stacks so that their applications can be served by WSGI servers, we hope you can see how fully Pylons embraces WSGI throughout its design to be the most flexible and extensible of the main Python web frameworks. 

To find out more about the Web Server Gateway Interface you might find the following resources useful: 

* `PEP 333 <http://www.python.org/dev/peps/pep-0333/>`_ 
* `The WSGI website at wsgi.org <http://wsgi.org>`_ 
* XML.com articles: Introducing WSGI - Pythons Secret Web Weapon.html `Part 1 <http://www.xml.com/pub/a/2006/09/27/introducing-wsgi-pythons-secret-web-weapon.html>`_ `Part 2 <http://www.xml.com/pub/a/2006/10/04/introducing-wsgi-pythons-secret-web-weapon-part-two.html>`_ 


.. _deployment:

Packaging and Deployment Overview
=================================

TODO: some of this is redundant to the (more current) :ref:`configuration` doc -- should be consolidated and cross-referenced

This document describes how a developer can take advantage of Pylons' application setup functionality to allow webmasters to easily set up their application. 

Installation refers to the process of downloading and installing the application with :term:`easy_install` whereas setup refers to the process of setting up an instance of an installed application so it is ready to be deployed. 

For example, a wiki application might need to create database tables to use. The webmaster would only install the wiki ``.egg`` file once using :term:`easy_install` but might want to run 5 wikis on the site so would setup the wiki 5 times, each time specifying a different database to use so that 5 wikis can run from the same code, but store their data in different databases. 

Egg Files
*********

Before you can understand how a user configures an application you have to understand how Pylons applications are distributed. All Pylons applications are distributed in ``.egg`` format. An egg is simply a Python executable package that has been put together into a single file. 

You create an egg from your project by going into the project root directory and running the command: 

.. code-block:: bash 

    $ python setup.py bdist_egg 

If everything goes smoothly a ``.egg`` file with the correct name and version number appears in a newly created ``dist`` directory. 

When a webmaster wants to install a Pylons application he will do so by downloading the egg and then installing it. 

Installing as a Non-root User
*****************************

It's quite possible when using shared hosting accounts that you do not have root access to install packages. In this case you can install :term:`setuptools` based packages like Pylons and Pylons web applications in your home directory using a :term:`virtualenv` setup. This way you can install all the packages you want to use without super-user access. 

Understanding the Setup Process 
*******************************

Say you have written a Pylons wiki application called ``wiki``. When a webmaster wants to install your wiki application he will run the following command to generate a config file: 

.. code-block:: bash 

    $ paster make-config wiki wiki_production.ini 

He will then edit the config file for his production environment with the settings he wants and then run this command to setup the application: 

.. code-block:: bash 

    $ paster setup-app wiki_production.ini 

Finally he might choose to deploy the wiki application through the paste server like this (although he could have chosen CGI/FastCGI/SCGI etc): 

.. code-block:: bash 

    $ paster serve wiki_production.ini 

The idea is that an application only needs to be installed once but if necessary can be set up multiple times, each with a different configuration. 

All Pylons applications are installed in the same way, so you as the developer need to know how the above commands work. 

Make Config 
----------- 

The ``paster make-config`` command looks for the file ``deployment.ini_tmpl`` and uses it as a basis for generating a new ``.ini`` file. 

Using our new wiki example again, the ``wiki/config/deployment.ini_tmpl`` file contains the text: 

.. code-block:: ini 

    [DEFAULT]
    debug = true
    email_to = you@yourdomain.com
    smtp_server = localhost
    error_email_from = paste@localhost

    [server:main]
    use = egg:Paste#http
    host = 0.0.0.0
    port = 5000

    [app:main]
    use = egg:wiki
    full_stack = true
    static_files = true
    cache_dir = %(here)s/data
    beaker.session.key = wiki
    beaker.session.secret = ${app_instance_secret}
    app_instance_uuid = ${app_instance_uuid}

    # If you'd like to fine-tune the individual locations of the cache data dirs
    # for the Cache data, or the Session saves, un-comment the desired settings
    # here:
    #beaker.cache.data_dir = %(here)s/data/cache
    #beaker.session.data_dir = %(here)s/data/sessions

    # WARNING: *THE LINE BELOW MUST BE UNCOMMENTED ON A PRODUCTION ENVIRONMENT*
    # Debug mode will enable the interactive debugging tool, allowing ANYONE to
    # execute malicious code after an exception is raised.
    set debug = false


    # Logging configuration
    [loggers]
    keys = root

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = INFO
    handlers = console

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(asctime)s %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s


When the command ``paster make-config wiki wiki_production.ini`` is run, the contents of this file are produced so you should tweak this file to provide sensible default configuration for production deployment of your app. 

Setup App 
--------- 

The ``paster setup-app`` command references the newly created ``.ini`` file and calls the function ``wiki.websetup.setup_app()`` to set up the application. If your application needs to be set up before it can be used, you should edit the ``websetup.py`` file. 

Here's an example which just prints the location of the cache directory via Python's logging facilities: 

.. code-block:: python 

    """Setup the helloworld application""" 
    import logging 

    from pylons import config
    from helloworld.config.environment import load_environment 

    log = logging.getLogger(__name__) 

    def setup_app(command, conf, vars): 
        """Place any commands to setup helloworld here""" 
        load_environment(conf.global_conf, conf.local_conf) 
        log.info("Using cache dirctory %s" % config['cache.dir']) 

For a more useful example, say your application needs a database set up and loaded with initial data. The user will specify the location of the database to use by editing the config file before running the ``paster setup-app`` command. The ``setup_app()`` function will then be able to load the configuration and act on it in the function body. This way, the ``setup_app()`` function can be used to initialize the database when ``paster setup-app`` is run. Using the optional :term:`SQLAlchemy` project template support when creating a Pylons project will set all of this up for you in a basic way. The :ref:`quickwiki_tutorial` illustrates an example of this configuration.

Deploying the Application
*************************

Once the application is setup it is ready to be deployed. There are lots of ways of deploying an application, one of which is to use the ``paster serve`` command which takes the configuration file that has already been used to setup the application and serves it on a local HTTP server for production use: 

.. code-block:: bash 

    $ paster serve wiki_production.ini 

More information on Paste deployment options is available on the Paste website at http://pythonpaste.org. See :ref:`deployment_webservers` for alternative Pylons deployment scenarios.

Advanced Usage
**************

So far everything we have done has happened through the ``paste.script.appinstall.Installer`` class which looks for the ``deployment.ini_tmpl`` and ``websetup.py`` file and behaves accordingly. 

If you need more control over how your application is installed you can use your own installer class. Create a file, for example ``wiki/installer.py`` and code your new installer class in the file by deriving it from the existing one:

.. code-block:: python 

    from paste.script.appinstall import Installer 
    class MyInstaller(Installer): 
        pass 

You then override the functionality as necessary (have a look at the source code for ``Installer`` as a basis. You then change your application's ``setup.py`` file so that the ``paste.app_install`` entry point ``main`` points to your new installer: 

.. code-block:: python 

    entry_points=""" 
    ... 
    [paste.app_install] 
    main=wiki.installer:MyInstaller 
    ... 
    """, 

Depending on how you code your ``MyInstaller`` class you may not even need your ``websetup.py`` or ``deployment.ini_tmpl`` as you might have decided to create the ``.ini`` file and setup the application in an entirely different way. 


.. _deployment_webservers:

Running Pylons Apps with Other Web Servers
==========================================

This document assumes that you have already installed a Pylons web application, and :ref:`run-config` for it.  Pylons applications use `PasteDeploy <http://pythonpaste.org/deploy/>`_ to  start up your Pylons WSGI application, and can use the flup package to provide a Fast-CGI, SCGI, or AJP connection to it. 

Using Fast-CGI
**************

`Fast-CGI <http://fastcgi.com/>`_ is a gateway to connect web severs like `Apache <http://httpd.apache.org/>`_ and `lighttpd <http://lighttpd.net/>`_ to a CGI-style application. Out of the box, Pylons applications can run with Fast-CGI in either a threaded or forking mode. (Threaded is the recommended choice) 

Setting a Pylons application to use Fast-CGI is very easy, and merely requires you to change the config line like so: 

.. code-block:: ini 

    # default 
    [server:main] 
    use = egg:Paste#http 

    # Use Fastcgi threaded 
    [server:main] 
    use = egg:PasteScript#flup_fcgi_thread 
    host = 0.0.0.0 
    port = 6500 

Note that you will need to install the `flup <http://www.saddi.com/software/flup/dist/>`_ package, which can be 
installed via easy_install: 

.. code-block:: bash 

    $ easy_install -U flup 

The options in the config file are passed onto flup. The two common ways to run Fast CGI is either using a socket to listen for requests, or listening on a port/host which allows a webserver to send your requests to web applications on a different machine. 

To configure for a socket, your ``server:main`` section should look like this: 

.. code-block:: ini 

    [server:main] 
    use = egg:PasteScript#flup_fcgi_thread 
    socket = /location/to/app.socket 

If you want to listen on a host/port, the configuration cited in the first example will do the trick. 

Apache Configuration
********************

For this example, we will assume you're using Apache 2, though Apache 1 configuration will be very similar. First, make sure that you have the Apache `mod_fastcgi <http://fastcgi.com/mod_fastcgi/docs/mod_fastcgi.html>`_ module installed in 
your Apache. 

There will most likely be a section where you declare your FastCGI servers, and whether they're external: 

.. code-block:: apacheconf 

    <IfModule mod_fastcgi.c> 
    FastCgiIpcDir /tmp 
    FastCgiExternalServer /some/path/to/app/myapp.fcgi -host some.host.com:6200 
    </IfModule> 

In our example we'll assume you're going to run a Pylons web application listening on a host/port. Changing ``-host`` to ``-socket`` will let you use a Pylons web application listening on a socket. 

The filename you give in the second option does not need to physically exist on the webserver, URIs that Apache resolve to this filename will be handled by the FastCGI application. 

The other important line to ensure that your Apache webserver has is to indicate that fcgi scripts should be handled with Fast-CGI: 

.. code-block:: apacheconf 

    AddHandler fastcgi-script .fcgi 

Finally, to configure your website to use the Fast CGI application you will need to indicate the script to be used: 

.. code-block:: apacheconf 

    <VirtualHost *:80> 
        ServerAdmin george@monkey.com 
        ServerName monkey.com 
        ServerAlias www.monkey.com 
        DocumentRoot /some/path/to/app 

        ScriptAliasMatch ^(/.*)$ /some/path/to/app/myapp.fcgi$1 
    </VirtualHost> 

Other useful directives should be added as needed, for example, the ErrorLog directive, etc. This configuration will result in all requests being sent to your FastCGI application. 

PrefixMiddleware
****************

``PrefixMiddleware`` provides a way to manually override the root prefix (``SCRIPT_NAME``) of your application for certain situations. 

When running an application under a prefix (such as '``/james``') in FastCGI/apache, the ``SCRIPT_NAME`` environment variable is automatically set to to the appropriate value: '``/james``'. Pylons' URL generators such as ``url`` always take the ``SCRIPT_NAME`` value into account. 

One situation where ``PrefixMiddleware`` is required is when an application is accessed via a reverse proxy with a prefix. The application is accessed through the reverse proxy via the the URL prefix '``/james``', whereas the reverse proxy forwards those requests to the application at the prefix '``/``'. 

The reverse proxy, being an entirely separate web server, has no way of specifying the ``SCRIPT_NAME`` variable; it must be manually set by a ``PrefixMiddleware`` instance. Without setting ``SCRIPT_NAME``, ``url`` will generate URLs such as: '``/purchase_orders/1``', when it should be generating: '``/james/purchase_orders/1``'. 

To filter your application through a ``PrefixMiddleware`` instance, add the following to the '``[app:main]``' section of your .ini file: 

.. code-block :: ini 

    filter-with = proxy-prefix 

    [filter:proxy-prefix] 
    use = egg:PasteDeploy#prefix 
    prefix = /james 

The name ``proxy-prefix`` simply acts as an identifier of the filter section; feel free to rename it. 

These .ini settings are equivalent to adding the following to the end of your application's ``config/middleware.py``, right before the ``return app`` line: 

.. code-block :: python 

    # This app is served behind a proxy via the following prefix (SCRIPT_NAME) 
    app = PrefixMiddleware(app, global_conf, prefix='/james') 

This requires the additional import line: 

.. code-block :: python 

    from paste.deploy.config import PrefixMiddleware 

Whereas the modification to ``config/middleware.py`` will setup an instance of ``PrefixMiddleware`` under every environment (.ini).

Using Java Web Servers with Jython
**********************************

See :ref:`java_deployment`.

.. _adding_documentation:

Documenting Your Application
============================

TODO: this needs to be rewritten -- Pudge is effectively dead

While the information in this document should be correct, it may not be entirely complete... Pudge is somewhat unruly to work with at this time, and you may need to experiment to find a working combination of package versions. In particular, it has been noted that an older version of Kid, like 0.9.1, may be required. You might also need to install {{RuleDispatch}} if you get errors related to {{FormEncode}} when attempting to build documentation. 

Apologies for this suboptimal situation. Considerations are being taken to fix Pudge or supplant it for future versions of Pylons. 

Introduction
************

Pylons comes with support for automatic documentation generation tools like `Pudge <http://pudge.lesscode.org>`_. 

Automatic documentation generation allows you to write your main documentation in the docs directory of your project as well as throughout the code itself using docstrings. 

When you run a simple command all the documentation is built into sophisticated HTML. 

Tutorial
********

First create a project as described in :ref:`getting_started`.

You will notice a docs directory within your main project directory. This is where you should write your main documentation. 

There is already an ``index.txt`` file in ``docs`` so you can already generate documentation. First we'll install Pudge and buildutils. By default, Pylons sets an option to use `Pygments <http://pygments.org>`_ for syntax-highlighting of code in your documentation, so you'll need to install it too (unless you wish to remove the option from ``setup.cfg``): 

.. code-block:: bash 

    $ easy_install pudge buildutils 
    $ easy_install Pygments 

then run the following command from your project's main directory where the ``setup.py`` file is: 

.. code-block:: bash 

    $ python setup.py pudge 

.. Note:: 

    The ``pudge`` command is currently disabled by default. Run the following command first to enable it: 

    ..code-block:: bash 

        $ python setup.py addcommand -p buildutils.pudge_command 

    Thanks to Yannick Gingras for the tip. 

Pudge will produce output similar to the following to tell you what it is doing and show you any problems: 

.. code-block:: text

    running pudge 
    generating documentation 
    copying: pudge\template\pythonpaste.org\rst.css -> do/docs/html\rst.css 
    copying: pudge\template\base\pudge.css -> do/docs/html\pudge.css 
    copying: pudge\template\pythonpaste.org\layout.css -> do/docs/html\layout.css 
    rendering: pudge\template\pythonpaste.org\site.css.kid -> site.css 
    colorizing: do/docs/html\do/__init__.py.html 
    colorizing: do/docs/html\do/tests/__init__.py.html 
    colorizing: do/docs/html\do/i18n/__init__.py.html 
    colorizing: do/docs/html\do/lib/__init__.py.html 
    colorizing: do/docs/html\do/controllers/__init__.py.html 
    colorizing: do/docs/html\do/model.py.html 

Once finished you will notice a ``docs/html`` directory. The ``index.html`` is the main file which was generated from ``docs/index.txt``. 

Learning ReStructuredText
*************************

Python programs typically use a rather odd format for documentation called `reStructuredText`_. It is designed so that the text file used to generate the HTML is as readable as possible but as a result can be a bit confusing for beginners. 

Read the reStructuredText tutorial which is part of the `docutils <http://docutils.sf.net>`_ project. 

Once you have mastered reStructuredText you can write documentation until your heart's content. 

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

Using Docstrings
****************

Docstrings are one of Python's most useful features if used properly. They are described in detail in the Python documentation but basically allow you to document any module, class, method or function, in fact just about anything. Users can then access this documentation interactively. 

Try this: 

.. code-block:: pycon

    >>> import pylons 
    >>> help(pylons) 
    ... 

As you can see if you tried it you get detailed information about the pylons module including the information in the docstring. 

Docstrings are also extracted by Pudge so you can describe how to use all the controllers, actions and modules that make up your application. Pudge will extract that information and turn it into useful API documentation automatically. 

Try clicking the ``Modules`` link in the HTML documentation you generated earlier or look at the Pylons source code for some examples of how to use docstrings. 

Using doctest
*************

The final useful thing about docstrings is that you can use the ``doctest`` module with them. ``doctest`` again is described in the Python documentation but it looks through your docstrings for things that look like Python code written at a Python prompt. Consider this example: 

.. code-block:: pycon 

    >>> a = 2 
    >>> b = 3 
    >>> a + b 
    5 

If ``doctest`` was run on this file it would have found the example above and executed it. If when the expression ``a + b`` is executed the result was not ``5``, ``doctest`` would raise an Exception. 

This is a very handy way of checking that the examples in your documentation are actually correct. 

To run ``doctest`` on a module use: 

.. code-block:: python 

    if __name__ == "__main__": 
        import doctest 
        doctest.testmod() 

The ``if __name__ == "__main__":`` part ensures that your module won't be tested if it is just imported, only if it is run from the command line 

To run ``doctest`` on a file use: 

.. code-block:: python 

    import doctest 
    doctest.testfile("docs/index.txt") 

You might consider incorporating this functionality in your ``tests/test.py`` file to improve the testing of your application. 

Summary
*******

So if you write your documentation in reStructuredText, in the ``docs`` directory and in your code's docstrings, liberally scattered with example code, Pylons provides a very useful and powerful system for you. 

If you want to find out more information have a look at the Pudge documentation or try tinkering with your project's ``setup.cfg`` file which contains the Pudge settings. 


.. _app_distribution:

Distributing Your Application
=============================

TODO: this assumes helloworld tutorial context that is no longer present, and could be consolidated with packaging info in :ref:`deployment`

As mentioned earlier eggs are a convenient format for packaging applications. You can create an egg for your project like this:

.. code-block:: bash

    $ cd helloworld
    $ python setup.py bdist_egg

Your egg will be in the ``dist`` directory and will be called ``helloworld-0.0.0dev-py2.4.egg``.

You can change options in ``setup.py`` to change information about your project. For example change version to ``version="0.1.0",`` and run ``python setup.py bdist_egg`` again to produce a new egg with an updated version number.

You can then register your application with the `Python Package Index`_ (PyPI) with the following command:

.. code-block:: bash

    $ python setup.py register

.. note::

    You should not do this unless you actually want to register a package!

If users want to install your software and have installed :term:`easy_install` they can install your new egg as follows:

.. code-block:: bash

    $ easy_install helloworld==0.1.0

This will retrieve the package from PyPI and install it. Alternatively you can install the egg locally:

.. code-block:: bash

    $ easy_install -f C:\path\with\the\egg\files\in helloworld==0.1.0

In order to use the egg in a website you need to use Paste. You have already used Paste to create your Pylons template and to run a test server to test the tutorial application.

Paste is a set of tools available at http://pythonpaste.org for providing a uniform way in which all compatible Python web frameworks can work together. To run a paste application such as any Pylons application you need to create a Paste configuration file. The idea is that the your paste configuration file will contain all the configuration for all the different Paste applications you run. A configuration file suitable for development is in the ``helloworld/development.ini`` file of the tutorial but the idea is that the person using your egg will add relevant configuration options to their own Paste configuration file so that your egg behaves they way they want. See the section below for more on this configuration.

Paste configuration files can be run in many different ways, from CGI scripts, as standalone servers, with FastCGI, SCGI, mod_python and more. This flexibility means that your Pylons application can be run in virtually any environment and also take advantage of the speed benefits that the deployment option offers.

.. seealso::

    :ref:`deployment_webservers`

.. _Python Package Index: http://pypi.python.org/pypi

Running Your Application
************************

In order to run your application your users will need to install it as described above but then generate a config file and setup your application before deploying it. This is described in :ref:`run-config` and :ref:`deployment`.

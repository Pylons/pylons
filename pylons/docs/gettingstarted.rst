.. _getting-started:

Getting Started
===============

Pylons is a MVC (Model-View-Controller) based approach to writing Python web
applications. While Pylons encourages and allows for a wide variety of popular
Python libraries, the documentation and recommendations by the Pylons 
developers covers 'best of breed' components chosen with the goal of
expressiveness, efficiency, and performance.

The two components people will care the most about are the templating
language and the database object relational mapper. While Pylons doesn't need
either to function, the following choices are recommended for new users:

* Models: `SQLAlchemy <http://www.sqlalchemy.org/>`_
* Templating: `Mako <http://www.makotemplates.org/>`_


Requirements
------------

* Python 2.3+ (Python 2.4+ highly recommended)


Installing
----------

.. warning::
    
    These instructions require the use of Python 2.4+. For installing on
    Python 2.3, please see :ref:`python2.3-installation`.

To avoid conflicts with system-installed Python libraries, Pylons comes with a
boot-strap Python script that sets up a `virtual environment <http://http://pypi.python.org/pypi/virtualenv>`_. Pylons will then be
installed under the virtual environment and ask if you'd like to create a new
Pylons project.

.. admonition:: Tip
    
    virtualenv is a handy tool to create isolated Python environments. In 
    addition to isolating packages from possible system conflicts, it makes
    it easy to install Python libraries with `easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ without dumping lots
    of packages into the system Python.
    
    The other great side-effect, is that no root access is required since all
    modules are kept under a directory of your choosing. This makes it easy
    to setup a working Pylons install on shared hosting providers and other
    systems where you might not have system-wide access.

1. Download the `go-pylons.py <http://www.pylonshq.com/download/go-pylons.py>`_ script.
2. Run the script and specify a directory for the virtual environment to be created under:
    
    .. code-block:: bash
        
        $ python go-pylons.py mydevenv

This will leave you with a functional virtualenv and Pylons installation.
Scripts using this environment can be run directly from it by specifying the
full path, ie:

.. code-block:: bash
    
    $ mydevenv/bin/paster --help


Creating a Pylons Project
-------------------------

Assuming you didn't opt to make a new project in the previous step, you may
create a new project named ``helloworld`` with the following command:

.. code-block:: bash

    $ paster create -t pylons helloworld

.. note:: 
    
    Windows users must configure their ``PATH`` as described in :ref:`windows-notes`, otherwise they must specify the full path name to the ``paster`` command.

This creates a new Pylons project which you can use as a basis for your own project. The directory structure is as follows:

.. code-block:: text

    - helloworld
        - README.txt
        - data
        - docs
        - development.ini
        - helloworld
        - helloworld.egg-info
            - Various files including paste_deploy_config.ini_tmpl
        - setup.cfg
        - setup.py
        - test.ini

The :file:`setup.py` file is used to create a re-distributable Python package of your project called an `egg <http://peak.telecommunity.com/DevCenter/PythonEggs>`_. Eggs can be thought of as similar to ``.jar`` files in Java. The :file:`setup.cfg` file contains extra information about your project and the ``helloworld.egg-info`` directory contains information about the egg.

You may also notice a ``data`` directory which is created the first time you run your application. You can configure the location of the ``data`` directory by editing your ``development.ini`` file. This directory will hold cached data and sessions used by your app while its running.

The ``helloworld`` directory within the ``helloworld`` directory is where all your application specific code and files are placed. The directory looks like this:

.. code-block:: text

    - helloworld
        - helloworld
            - config
            - controllers
            - lib
            - model
            - public
            - templates
            - tests
            - __init__.py
            - websetup.py

The ``config`` directory contains the configuration options for your web application.

The ``controllers`` directory is where your application controllers are written. Controllers are the core of your application where the decision is made on what data to load, and how to view it.

The ``lib`` directory is where you can put code that is used between different controllers, third party code, or any other code that doesn't fit in well elsewhere.

The ``model`` directory is for your model objects, if you're using an ORM this is where the classes for them should go. The database configuration string can be set in your ``development.ini`` file.

The ``public`` directory is where you put all your HTML, images, Javascript, CSS and other static files. It is similar to the htdocs directory in Apache.

The ``tests`` directory is where you can put controller and other tests. The controller testing functionality uses Nose and ``paste.fixture``. 

The ``templates`` directory is where templates are stored. Templates contain a mixture of plain text and Python code and are used for creating HTML and other documents in a way that is easy for designers to tweak without them needing to see all the code that goes on behind the scenes. Pylons uses Mako templates by default but can render templates in other template languages using the easy-to-extend render functions
provided in :ref:`custom-render`.

The ``__init__.py`` file is present so that the ``helloworld`` directory can be used as a Python module within the egg.

The ``websetup.py`` should contain any code that should be executed when an end user of your application runs the ``paster setup-app`` command described in  `Application Setup <Packaging+and+Deployment>`_. If you're looking for where to put that should be run before your application is, this is the place.


Running the application
-----------------------

We can now run the web application like this:
    
.. code-block:: bash

    $ cd helloworld
    $ paster serve --reload development.ini
    
The command loads our project server configuration file in :file:`development.ini` and serves the Pylons application.

The ``--reload`` option ensures that the server is automatically reloaded if
you make any changes to Python files or the :file:`development.ini` 
config file. This is very useful during development. To stop the server you
can press :command:`Ctrl+c` or your platform's equivalent.

If you visit http://127.0.0.1:5000/ when the server is running you will see the
welcome page (``127.0.0.1`` is a special IP address that references your own
computer but you can change the hostname by editing the
:file:`development.ini` file).

Try creating a new file named :file:`test.html` in the ``helloworld/public`` directory with the following content:

.. code-block:: html

    <html>
        <body>
            Hello World!
        </body>
    </html>
    
If you visit http://127.0.0.1:5000/test.html you will see the message ``Hello World!``. Any files in the ``public`` directory are served in the same way they would be by any webserver, but with built-in caching, and if Pylons has a choice of whether to serve a file from the ``public`` directory or from code in a controller it will always choose the file in ``public``. This behavior can be changed by altering the order of the ``Cascade`` in ``config/middleware.py``.


Interactive Debugger
--------------------

The interactive debugger is a powerful tool for use during application development. It is enabled by default in the development environment's ``development.ini``. When enabled, it allows debugging of the application through a web page after an exception is raised. On production environments the debugger poses a major security risk; so production ini files generated from the ``paster make-config`` command will have debugging disabled.

To disable debugging, uncomment the following line in the ``[app:main]`` section of your ``development.ini``:

.. code-block:: ini

    #set debug = false
    
to:

.. code-block:: ini

    set debug = false

Again; debug must be set to false on production environments as the interactive debugger poses a MAJOR SECURITY RISK.

More information is available in the `Interactive Debugger <Interactive+Application+Debugging>`_ documentation.



Hello World
-----------




Rendering a Template
--------------------


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

.. admonition:: By The Way
    
    virtualenv is a handy tool to create isolated Python environments. In 
    addition to isolating packages from possible system conflicts, it makes
    it easy to install Python libraries using `easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ without dumping lots
    of packages into the system-wide Python.
    
    The other great benefit, is that no root access is required since all
    modules are kept under a directory of your choosing. This makes it easy
    to setup a working Pylons install on shared hosting providers and other
    systems where you might not have system-wide access.

1. Download the `go-pylons.py <http://www.pylonshq.com/download/0.9.7/go-pylons.py>`_ script.
2. Run the script and specify a directory for the virtual environment to be created under:
    
    .. code-block:: bash
        
        $ python go-pylons.py mydevenv

.. admonition:: Tip
    
    The two steps can be combined on unix systems with curl using the
    following short-cut:
    
    .. code-block:: bash
    
        $ curl http://pylonshq.com/download/0.9.7/go-pylons.py | python - mydevenv
    
    To isolate further from additional system-wide Python libraries, run
    with the no site packages option:
    
    .. code-block:: bash
    
        $ python go-pylons.py --no-site-packages mydevenv

This will leave you with a functional virtualenv and Pylons installation.
Activate the virtual environment (scripts may also be run by specifying the
full path to the mydevenv/bin dir):

.. code-block:: bash

    $ source mydevenv/bin/activate

Or on Window to activate:

.. code-block:: text
    
    > mydevenv\bin\activate.bat


Creating a Pylons Project
-------------------------

Create a new project named ``helloworld`` with the following command:

.. code-block:: bash

    $ paster create -t pylons helloworld

.. note:: 
    
    Windows users must configure their ``PATH`` as described in :ref:`windows-notes`, otherwise they must specify the full path name to the ``paster`` command (including the virtual environment bin dir).

Running this will prompt you for two choices, whether or not to include 
:term:`SQLAlchemy` support, and which template language to use. Hit enter both times
to accept the defaults (no :term:`SQLAlchemy`, with Mako templating). 

The created directory structure with links to more information:

- helloworld
    - MANIFEST.in
    - README.txt
    - development.ini - :ref:`run-config`
    - docs
    - ez_setup.py
    - helloworld
        - __init__.py
        - config - :ref:`app-config`
        - controllers - :ref:`controllers`
        - lib
        - model - :ref:`models`
        - public
        - templates - :ref:`templates`
        - tests
        - websetup.py
    - helloworld.egg-info
    - setup.cfg
    - setup.py - :ref:`setup-config`
    - test.ini


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


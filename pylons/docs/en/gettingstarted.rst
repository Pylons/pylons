.. _getting_started:

===============
Getting Started
===============

This section is intended to get Pylons up and running as fast as
possible and provide a quick overview of the project. Links are provided
throughout to encourage exploration of the various aspects of Pylons.


************
Requirements
************

* Python 2 series above and including 2.4 (Python 3 or later not supported at 
    this time)


.. _installing_pylons:

**********
Installing
**********

To avoid conflicts with system-installed Python libraries, Pylons comes with a
boot-strap Python script that sets up a "virtual" Python environment. Pylons will then be installed under the virtual environment.

.. admonition:: By the Way
    
    :term:`virtualenv` is a useful tool to create isolated Python environments.
    In addition to isolating packages from possible system conflicts, it makes
    it easy to install Python libraries using :term:`easy_install` without
    dumping lots of packages into the system-wide Python.
    
    The other great benefit is that no root access is required since all
    modules are kept under the desired directory. This makes it easy
    to setup a working Pylons install on shared hosting providers and other
    systems where system-wide access is unavailable.

1. Download the `go-pylons.py <http://www.pylonshq.com/download/1.0/go-pylons.py>`_ script.
2. Run the script and specify a directory for the virtual environment to be created under:
    
    .. code-block:: bash
        
        $ python go-pylons.py mydevenv

.. admonition:: Tip
    
    The two steps can be combined on unix systems with curl using the
    following short-cut:
    
    .. code-block:: bash
    
        $ curl http://pylonshq.com/download/1.0/go-pylons.py | python - mydevenv
    
    To isolate further from additional system-wide Python libraries, run
    with the --no-site-packages option:
    
    .. code-block:: bash
    
        $ python go-pylons.py --no-site-packages mydevenv
    
    | **How it Works**
    
    The ``go-pylons.py`` script is little more than a basic :term:`virtualenv`
    bootstrap script, that then does ``easy_install Pylons==1.0``. You could
    do the equivilant steps by manually fetching the ``virtualenv.py`` script
    and then installing Pylons like so:
    
    .. code-block:: bash
        
        curl -O http://bitbucket.org/ianb/virtualenv/raw/8dd7663d9811/virtualenv.py
        python virtualenv.py mydevenv
        mydevenv/bin/easy_install Pylons==1.0
    

This will leave a functional virtualenv and Pylons installation.
    
    
Activate the virtual environment (scripts may also be run by specifying the
full path to the mydevenv/bin dir):

.. code-block:: bash

    $ source mydevenv/bin/activate

Or on Window to activate:

.. code-block:: text
    
    > mydevenv\Scripts\activate.bat

.. note::
    
    If you get an error such as::
        
        ImportError: No module named _md5
    
    during the install. It is likely that your Python installation is missing
    standard libraries needed to run Pylons. Debian and other systems using
    debian packages most frequently encounter this, make sure to install
    the ``python-dev`` packages and ``python-hashlib`` packages.


Working Directly From the Source Code 
=====================================

`Mercurial <http://www.selenic.com/mercurial/wiki/>`_ must be installed to retrieve the latest development source for Pylons. `Mercurial packages <http://www.selenic.com/mercurial/wiki/index.cgi/BinaryPackages>`_ are also available for Windows, MacOSX, and other OS's. 

Check out the latest code: 

.. code-block:: bash 

    $ hg clone http://bitbucket.org/bbangert/pylons/

To tell setuptools to use the version in the ``Pylons`` directory: 

.. code-block:: bash 

    $ cd pylons 
    $ python setup.py develop 

The active version of Pylons is now the copy in this directory, and changes made there will be reflected for Pylons apps running.


*************************
Creating a Pylons Project
*************************

Create a new project named ``helloworld`` with the following command:

.. code-block:: bash

    $ paster create -t pylons helloworld

.. note:: 
    
    Windows users must configure their ``PATH`` as described in :ref:`windows_notes`, otherwise they must specify the full path to the ``paster`` command (including the virtual environment bin directory).

Running this will prompt for two choices:

1. which templating engine to use
2. whether to include :term:`SQLAlchemy` support

Hit enter at each prompt to accept the defaults (Mako templating, no :term:`SQLAlchemy`). 

Here is the created directory structure with links to more information:

- helloworld
    - MANIFEST.in
    - README.txt
    - development.ini - :ref:`run-config`
    - docs
    - ez_setup.py
    - helloworld (See the nested :ref:`helloworld directory <helloworld_dir>`)
    - helloworld.egg-info
    - setup.cfg
    - setup.py - :ref:`setup-config`
    - test.ini

.. _helloworld_dir:

The nested ``helloworld directory`` looks like this:

- helloworld
    - __init__.py
    - config
        - environment.py - :ref:`environment-config`
        - middleware.py - :ref:`middleware-config`
        - routing.py - :ref:`url-config`
    - controllers - :ref:`controllers`
    - lib
        - app_globals.py - :term:`app_globals`
        - base.py
        - helpers.py - :ref:`helpers`
    - model - :ref:`models`
    - public
    - templates - :ref:`templates`
    - tests - :ref:`testing`
    - websetup.py - :ref:`run-config`



***********************
Running the application
***********************

Run the web application:

.. code-block:: bash

    $ cd helloworld
    $ paster serve --reload development.ini
    
The command loads the project's server configuration file in :file:`development.ini` and serves the Pylons application.

.. note::
    
    The ``--reload`` option ensures that the server is automatically reloaded
    if changes are made to Python files or the :file:`development.ini` 
    config file. This is very useful during development. To stop the server
    press :command:`Ctrl+c` or the platform's equivalent.
    
    The paster serve command can be run anywhere, as long as the 
    development.ini path is properly specified. Generally during development
    it's run in the root directory of the project.

Visiting http://127.0.0.1:5000/ when the server is running will show the welcome page.


***********
Hello World
***********

To create the basic hello world application, first create a
:term:`controller` in the project to handle requests:

.. code-block:: bash

    $ paster controller hello

Open the :file:`helloworld/controllers/hello.py` module that was created.
The default controller will return just the string 'Hello World':

.. code-block:: python

    import logging

    from pylons import request, response, session, tmpl_context as c, url
    from pylons.controllers.util import abort, redirect

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)
    
    class HelloController(BaseController):

        def index(self):
            # Return a rendered template
            #return render('/hello.mako')
            # or, Return a response
            return 'Hello World'

At the top of the module, some commonly used objects are imported automatically.

Navigate to http://127.0.0.1:5000/hello/index where there should be a short text string saying "Hello World" (start up the app if needed):

.. image:: _static/helloworld.png

.. admonition:: Tip
    
    :ref:`url-config` explains how URL's get mapped to controllers and
    their methods.

Add a template to render some of the information that's in the :term:`environ`.

First, create a :file:`hello.mako` file in the :file:`templates`
directory with the following contents:

.. code-block:: mako

    Hello World, the environ variable looks like: <br />
    
    ${request.environ}

The :term:`request` variable in templates is used to get information about the current request. :ref:`Template globals <template-globals>` lists all the variables Pylons makes available for use in templates.

Next, update the :file:`controllers/hello.py` module so that the
index method is as follows:

.. code-block:: python

    class HelloController(BaseController):

        def index(self):
            return render('/hello.mako')

Refreshing the page in the browser will now look similar to this:

.. image:: _static/hellotemplate.png

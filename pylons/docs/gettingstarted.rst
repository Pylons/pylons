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

.. note:: 
    
    Python 2.4+ is highly recommended and is needed for the recommended
    installation method using the bootstrap script.


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

Hello World
-----------

Rendering a Template
--------------------



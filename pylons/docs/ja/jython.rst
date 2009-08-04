.. _jython:

================
Pylons on Jython
================

Pylons supports `Jython <http://www.jython.org>`_ as of v0.9.7.

Installation
============

The installation process is the same as CPython, as described in
:ref:`getting_started`. At least Jython 2.5b2 is required.

.. _java_deployment:

Deploying to Java Web servers
=============================

The Java platform defines the `Servlet API`_ for creating web applications. The
`modjy`_ library included with Jython provides a gateway between Java Servlets
and WSGI applications.

The `snakefight`_ tool can create a `WAR file`_ from a Pylons application (and
modjy) that's suitable for deployment to the various `Servlet containers`_ (such
as `Apache Tomcat`_ or `Sun's Glassfish`_).

Creating .wars with snakefight
------------------------------

First, install snakefight:

.. code-block :: bash

    $ easy_install snakefight

This adds an additional command to distutils: :command:`bdist_war`.

Pylons applications are loaded from Paste, via its ``paste.app_factory`` entry
point and a Paste style configuration file. :command:`bdist_war` knows how to
setup Paste apps for deployment when specified the :option:`--paste-config`
option:

.. code-block :: bash

    $ paster make-config MyApp production.ini
    $ jython setup.py bdist_war --paste-config production.ini

As with any distutils command the preferred options can instead be added to the
:file:`setup.cfg` in the root directory of the project:

.. code-block :: ini

    [bdist_war]
    paste-config = production.ini

Then we can simply run:

.. code-block :: bash

    $ jython setup.py bdist_war

:command:`bdist_war` creates a :file:`.war` with the following:

- Jython's :file:`jar` files in :file:`WEB-INF/lib`
- Jython's stdlib in :file:`WEB-INF/lib-python`
- Your application's required eggs in :file:`WEB-INF/lib-python`

With the :option:`--paste-config` option, it also:

- Creates a simple loader for the application/config
- Generates a :file:`web.xml` deployment descriptor configuring modjy to load
  the application with the simple loader

For further information/usages, see `snakefight's documentation`_.


.. _`Servlet API`: http://en.wikipedia.org/wiki/Java_Servlet
.. _`modjy`: http://modjy.xhaus.com/
.. _`snakefight`: http://pypi.python.org/pypi/snakefight
.. _`snakefight's documentation`: http://pypi.python.org/pypi/snakefight
.. _`WAR file`: http://en.wikipedia.org/wiki/Sun_WAR_(file_format)
.. _`Servlet containers`: http://en.wikipedia.org/wiki/Servlet_container
.. _`Apache Tomcat`: http://tomcat.apache.org/
.. _`Sun's Glassfish`: http://glassfish.org/

.. _glossary:

Glossary
========

.. glossary::

    action
        The class method in a Pylons applications' controller that handles
        a request.

    API
        Application Programming Interface. The means of communication between
        a programmer and a software program or operating system.

    app_globals
        The ``app_globals`` object is created on application instantiation by
        the :class:`Globals` class in a projects :file:`lib/app_globals.py`
        module.

        This object is created once when the application is loaded by the
        projects :file:`config/environment.py` module (See
        :ref:`environment-config`). It remains persistent
        during the lifecycle of the web application, and is *not* thread-safe
        which means that it is best used for global options that should be
        *read-only*, or as an object to attach db connections or other objects
        which ensure their own access is thread-safe.

    c
        Commonly used alias for :term:`tmpl_context` to save on the typing
        when using lots of controller populated variables in templates.

    caching
        The storage of the results of expensive or length computations for
        later re-use at a point more quickly accessed by the end user.

    CDN
        Content Delivery Networks (CDN's) are generally globally distributed
        content delivery networks optimized for low latency for static file
        distribution. They can significantly increase page-load times by
        ensuring that the static resources on a page are delivered by servers
        geographically close to the client in addition to lightening the load
        placed on the application server.

    ColdFusion Components
        CFCs represent an attempt by Macromedia to bring ColdFusion closer
        to an Object Oriented Programming (OOP) language. ColdFusion is in
        no way an OOP language, but thanks in part to CFCs, it does boast
        some of the attributes that make OOP languages so popular.

    
    config
        The :class:`~pylons.configuration.PylonsConfig` instance for a given
        application. This can be accessed as ``pylons.config`` after an 
        Pylons application has been loaded.
    
    controller
        The 'C' in MVC. The controller is given a request, does the necessary
        logic to prepare data for display, then renders a template with
        the data and returns it to the user. See :ref:`controllers`.

    easy_install
        A tool that lets you download, build, install and manage Python packages
        and their dependencies. `easy_install`_ is the end-user facing component
        of :term:`setuptools`.

        Pylons can be installed with ``easy_install``, and applications built
        with Pylons can easily be deployed this way as well.

        .. seealso::
            Pylons :ref:`deployment`

        .. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
    
    dotted name string
        A reference to a Python module by name using a string to identify it,
        e.g. ``pylons.controllers.util``. These strings are evaluated to
        import the module being referenced without having to import it in
        the code used. This is generally used to avoid import-time 
        side-effects.
    
    egg
        Python egg's are bundled Python packages, generally installed by
        a package called :term:`setuptools`. Unlike normal Python package
        installs, egg's allow a few additional features, such as package
        dependencies, and dynamic discovery.

        .. seealso::
            `The Quick Guide to Python Eggs <http://peak.telecommunity.com/DevCenter/PythonEggs>`_

    EJBs
        Enterprise JavaBeans (EJB) technology is the server-side component
        architecture for Java Platform, Enterprise Edition (Java EE). EJB
        technology enables rapid and simplified development of distributed,
        transactional, secure and portable applications based on Java
        technology.

    environ
        environ is a dictionary passed into all :term:`WSGI` application. It
        generally contains unparsed header information, CGI style variables
        and other objects inserted by :term:`WSGI Middleware`.

    ETag
        An ETag (entity tag) is an HTTP response header returned by an
        HTTP/1.1 compliant web server used to determine change in content
        at a given URL. See http://wikipedia.org/wiki/HTTP_ETag

    g
        Alias used in prior versions of Pylons for :term:`app_globals`.

    Google App Engine
      A cloud computing platform for hosting web applications implemented in
      Python. Building Pylons applications for App Engine is facilitated by
      Ian Bicking's `appengine-monkey project <http://code.google.com/p/appengine-monkey/>`_.

      .. seealso::
        `What is Google App Engine? - Official Doc <http://code.google.com/appengine/docs/whatisgoogleappengine.html>`_

    h
        The helpers reference, ``h``, is made available for use inside
        templates to assist with common rendering tasks. ``h`` is just a
        reference to the :file:`lib/helpers.py` module and can be used in the
        same manner as any other module import.

    Model-View-Controller
        An architectural pattern used in software engineering. In Pylons, the
        MVC paradigm is extended slightly with a pipeline that may transform
        and extend the data available to a controller, as well as the Pylons
        :term:`WSGI` app itself that determines the appropriate Controller
        to call.

        .. seealso::
            `MVC at Wikipedia
            <http://wikipedia.org/wiki/Model-View-Controller>`_

    MVC
        See :term:`Model-View-Controller`

    ORM
        (Object-Relational Mapper) Maps relational databases such as
        MySQL, Postgres, Oracle to objects providing a cleaner API.
        Most ORM's also make it easier to prevent SQL Injection attacks
        by binding variables, and can handle generating sometimes
        extensive SQL.

    Pylons
        A Python-based WSGI oriented web framework.

    Rails
        Abbreviated as RoR, Ruby on Rails (also referred to as just
        Rails) is an open source Web application framework, written in Ruby

    request
        Refers to the current request being processed. Available to import
        from :mod:`pylons` and is available for use in templates by the
        same name. See :class:`~pylons.controllers.util.Request`.
    
    response
        Refers to the response to the current request. Available to import
        from :mod:`pylons` and is available for use in template by the same
        name. See :class:`~pylons.controllers.util.Response`.

    route
        Routes determine how the URL's are mapped to the controllers and which
        URL is generated. See :ref:`url-config`

    setuptools
        An extension to the basic distutils, setuptools allows packages to
        specify package dependencies and have dynamic discovery of other
        installed Python packages.

        .. seealso::
            `Building and Distributing Packages with setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_

    SQLAlchemy
        One of the most popular Python database object-relational mappers
        (:term:`ORM`). `SQLAlchemy <http://www.sqlalchemy.org/>`_ is the default
        ORM recommended in Pylons. SQLAlchemy at the ORM level can look similar
        to Rails ActiveRecord, but uses the `DataMapper <http://www.martinfowler.com/eaaCatalog/dataMapper.html>`_
        pattern for additional flexibility with the ability to map simple to
        extremely complex databases.

    tmpl_context
        The ``tmpl_context`` is available in the :mod:`pylons` module, and
        refers to the template context. Objects attached to it are available
        in the template namespace as either ``tmpl_context`` or ``c`` for
        convenience.

    UI
        User interface. The means of communication between a person
        and a software program or operating system.

    virtualenv
        A tool to create isolated Python environments, designed to supersede the
        ``workingenv`` package and `virtual python`_ configurations. In addition
        to isolating packages from possible system conflicts, `virtualenv`_
        makes it easy to install Python libraries using :term:`easy_install`
        without dumping lots of packages into the system-wide Python.

        The other great benefit is that no root access is required since all
        modules are kept under the desired directory. This makes it easy
        to setup a working Pylons install on shared hosting providers and other
        systems where system-wide access is unavailable.

        ``virtualenv`` is employed automatically by the ``go-pylons.py`` script
        described in :ref:`getting_started`. The Pylons wiki has more
        information on `working with virtualenv`_.

        .. _virtual python: http://peak.telecommunity.com/DevCenter/EasyInstall#creating-a-virtual-python
        .. _virtualenv: http://pypi.python.org/pypi/virtualenv
        .. _working with virtualenv: http://wiki.pylonshq.com/display/pylonscookbook/Using+a+Virtualenv+Sandbox

    web server gateway interface
        A specification for web servers and application servers to
        communicate with web applications. Also referred to by its
        initials, as :term:`WSGI`.

    WSGI
        The `WSGI Specification <http://www.python.org/dev/peps/pep-0333/>`_,
        also commonly referred to as PEP 333 and described by :pep:`333`.

    WSGI Middleware
        :term:`WSGI` Middleware refers to the ability of WSGI applications
        to modify the environ, and/or the content of other WSGI applications
        by being placed in between the request and the other WSGI application.

        .. seealso::
            :ref:`WSGI Middleware in Concepts of Pylons <wsgi-middleware>`
            :ref:`WSGI Middleware Configuration <middleware-config>`

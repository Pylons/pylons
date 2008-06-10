.. _glossary:

Glossary
========

.. glossary::
    
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

    ColdFusion Components
        CFCs represent an attempt by Macromedia to bring ColdFusion closer 
        to an Object Oriented Programming (OOP) language. ColdFusion is in 
        no way an OOP language, but thanks in part to CFCs, it does boast 
        some of the attributes that make OOP languages so popular.
    
    controller
        The 'C' in MVC. The controller is given a request, does the necessary
        logic to prepare data for display, then renders a template with
        the data and returns it to the user. See :ref:`controllers`.
    
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
    
    h
        The helpers reference, ``h``, is made available for use inside
        templates to assist with common rendering tasks. ``h`` is just a 
        reference to the :file:`lib/helpers.py` module and can be used in the
        same manner as any other module import.
    
    Model-View-Controller
        an architectural pattern used in software engineering. 
        See http://wikipedia.org/wiki/Model-View-Controller

    MVC
        See :term:`Model-View-Controller`
    
    Pylons
        A Python-based WSGI oriented web framework.
    
    Rails
        Abbreviated as RoR, Ruby on Rails (also referred to as just 
        Rails) is an open source Web application framework, written in Ruby

    request
        Refers to the current request being processed. Available to import
        from :mod:`pylons` and is available for use in templates by the
        same name. See :class:`~pylons.controllers.util.Request`.
    
    SQLAlchemy
        One of the most popular Python database object-relation mappers
        (ORM's). `SQLAlchemy <http://www.sqlalchemy.org/>`_ is the default
        ORM recommended in Pylons. SQLAlchemy at the ORM level can look
        similar to Rails ActiveRecord, but uses the
        `DataMapper <http://www.martinfowler.com/eaaCatalog/dataMapper.html>`_
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

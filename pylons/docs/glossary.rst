.. _glossary:

Glossary
========

.. glossary::
    
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
    
    controller
        The 'C' in MVC. The controller is given a request, does the necessary
        logic to prepare data for display, then renders a template with
        the data and returns it to the user. See :ref:`controllers`.
    
    g
        Alias used in prior versions of Pylons for :term:`app_globals`.
    
    h
        The helpers reference, ``h``, is made available for use inside
        templates to assist with common rendering tasks. ``h`` is just a 
        reference to the :file:`lib/helpers.py` module and can be used in the
        same manner as any other module import.
    
    Pylons
        A Python-based WSGI oriented web framework.
    
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

    WSGI
        The `WSGI Specification <http://www.python.org/dev/peps/pep-0333/>`_,
        also commonly referred to as PEP 333 and described by :pep:`333`.    

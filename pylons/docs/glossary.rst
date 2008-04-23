.. _glossary:

Glossary
========

.. glossary::
    
    app_globals
        **(Previously referred to as** ``g`` **)**
        
        The ``app_globals`` object is created on application instantiation by
        the :class:`Globals` class in a projects :file:`lib/app_globals.py`
        module.
    
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
        **(Also referred to as** ``c`` **)**
        
        The ``tmpl_context`` is available in the :mod:`pylons` module, and 
        refers to the template context. Objects attached to it are available
        in the template namespace as either ``tmpl_context`` or ``c`` for 
        convenience.

    WSGI
        The `WSGI Specification <http://www.python.org/dev/peps/pep-0333/>`_,
        also commonly referred to as PEP 333 and described by :pep:`333`.    

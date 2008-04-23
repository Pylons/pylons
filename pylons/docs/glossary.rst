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
    
    WSGI
        The `WSGI Specification <http://www.python.org/dev/peps/pep-0333/>`_,
        also commonly referred to as PEP 333 and described by :pep:`333`.
    
    tmpl_context
        **(Also referred to as** ``c`` **)**
        
        The ``tmpl_context`` is available in the :mod:`pylons` module, and 
        refers to the template context. Objects attached to it are available
        in the template namespace as either ``tmpl_context`` or ``c`` for 
        convenience.

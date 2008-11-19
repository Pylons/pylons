:mod:`pylons.middleware` -- WSGI Middleware
===========================================

.. automodule:: pylons.middleware

Module Contents
---------------

.. autoclass:: StatusCodeRedirect
    :members: __init__
.. autoclass:: StaticJavascripts
.. autofunction:: ErrorHandler

.. note::

    The :data:`errorware` dictionary is constructed from the settings in the `DEFAULT` section of development.ini. the recognised keys and settings at initialization are:
     * :data:`error_email` = conf.get('email_to')
     * :data:`error_log` = conf.get('error_log', None)
     * :data:`smtp_server` = conf.get('smtp_server','localhost')
     * :data:`error_subject_prefix` = conf.get('error_subject_prefix', 'WebApp Error: ')
     * :data:`from_address` = conf.get('from_address', conf.get('error_email_from', 'pylons@yourapp.com'))
     * :data:`error_message` = conf.get('error_message', 'An internal server error occurred')

Referenced classes
------------------
Pylons middleware uses :class:`WebError` to effect the error-handling. The two classes implicated are:

ErrorMiddleware
^^^^^^^^^^^^^^^

:mod:`weberror.errormiddleware`
:class:`weberror.errormiddleware.ErrorMiddleware`


EvalException
^^^^^^^^^^^^^

:mod:`weberror.evalexception`
:class:`weberror.evalexception.EvalException`

Legacy
------

.. versionchanged:: 0.9.7
    These functions were deprecated in Pylons 0.9.7, and have been superceded
    by the :class:`StatusCodeRedirect` middleware.

.. autofunction:: pylons.middleware.ErrorDocuments
.. autofunction:: pylons.middleware.error_mapper


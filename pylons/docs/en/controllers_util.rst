.. _controllers_util:

==================================================
Controller utilities, Request and Response objects
==================================================

The Request object
==================

The Request object for the current session is accessible when imported from Pylons:

.. code-block:: python

    from pylons import request

The Pylons request object is is a subclass of the WebOb :class:`webob.Request` class (see the :ref:`webob` section for full details) which has no charset, or other defaults. This subclass adds defaults, along with several methods for backwards compatibility with :class:`paste.wsgiwrappers.WSGIRequest`.

:func:`determine_browser_charset`
---------------------------------

This is a legacy method to return the :attr:`webob.Request.accept_charset`

:func:`languages`
-----------------

Return the best matching languages.

:func:`match_accept`
--------------------

Returns the first matching mimetype

:func:`signed_cookie`
---------------------

Takes args of ``name`` and ``secret`` and extracts a signed cookie of ``name`` from the request. The cookie is expected to have been created with ``Response.signed_cookie`` and the ``secret`` should be the same as the one used to sign it. Any failure in the signature of the data will result in ``None`` being returned.

The Response object
===================

The Response object for the current session is accessible when imported from Pylons:

.. code-block:: python

    from pylons import response

The Pylons request object is a subclass of the :class:`webob.Response` class (see the :ref:`webob` section for full details) which has no default content type, or error defaults. This subclass adds defaults, along with several methods for backwards compatibility with paste.wsgiwrappers.WSGIResponse.

:func:`determine_charset`
-------------------------

Return the charset.

:func:`has_header`
------------------

Takes arg of ``header`` and returns setting for ``header`` as in ``response.headers``.

:func:`get_content`
-------------------

Return the content of the response, retrieved from ``response.body``.

:func:`write`
----------------------------

Takes arg of ``content`` (a string or unicode string) and writes it into the response body.

:func:`wsgi_response`
---------------------

Returns multiple-valued response of status, headers and body.

:func:`signed_cookie`
---------------------

Takes args of ``name`` (the name of the storage key), ``data`` (the data to be stored) and keyworded arg ``secret`` (an optional signature). Saves a signed cookie of the pickled data with ``secret`` signature. All other keyword arguments that ``WebOb.set_cookie`` accepts are usable and passed to the WebOb set_cookie method after creating the signed cookie value.

Utility functions
=================

:func:`etag_cache`: using the HTTP Entity Tag cache for browser-side caching
----------------------------------------------------------------------------

.. note::
    Using the :func:`etag_cache` function is described in detail in the :ref:`caching` section.

Use the HTTP Entity Tag cache for Browser side caching. If a "If-None-Match" header is found, and equivalent to ``key``, then a ``304`` HTTP message will be returned with the ETag to tell the browser that it should use its current cache of the page. Otherwise, the ETag header will be added to the response headers. Returns ``pylons.response`` for legacy purposes (``pylons.response`` should be used directly instead).
    
Suggested use is within a Controller Action like so:

.. code-block:: python

    import pylons

    class YourController(BaseController):
        def index(self):
            etag_cache(key=1)
            return render('/splash.mako')

.. note::
    This works because etag_cache will raise an ``HTTPNotModified`` exception if the ETag received matches the key provided.
    

:func:`forward`: Forwarding requests to a WSGI application
----------------------------------------------------------

Takes an arg of a WSGI application and forwards the request to the WSGI application. Returns its response.

:func:`abort`: Aborting the request immediately by returning an HTTP exception
------------------------------------------------------------------------------

Takes keyword args: ``status_code``, ``detail``, ``headers`` and ``comment``. Aborts the request immediately by returning an HTTP exception. In the event that the status_code is a 300 series error, the ``detail`` attribute will be used as the ``Location`` header should one not be specified in the ``headers`` attribute.
    

``redirect``: Raising a redirect exception to a specified URL
-------------------------------------------------------------

Takes a URL as argument and raises a redirect exception to the specified URL. Optionally, a ``code`` variable may be passed with the status code of the redirect, ie:

.. code-block:: python

    redirect(url(controller='home', action='index'), code=303)


``redirect_to``: Raising a redirect exception to a URL resolved by Routes' :func:`url_for` function
---------------------------------------------------------------------------------------------------

**Deprecated**, use :func:`redirect` as listed above.

Raises a redirect exception to the URL resolved by Routes' :func:`url_for` function. Optionally, a ``_code`` keyword arg may be passed with the status code of the redirect, i.e.:

.. code-block:: python

    redirect_to(controller='home', action='index', _code=303)


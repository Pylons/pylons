.. _paster:

WSGI, CLI scripts
=================

Working with :class:`wsgiwrappers.WSGIRequest`
----------------------------------------------

Pylons uses a specialised *WSGIRequest* class that is accessible via the
``paste.wsgiwrappers`` module.

The ``wsgiwrappers.WSGIRequest`` object represents a WSGI request that has 
a more programmer-friendly interface. This interface does not expose every 
detail of the WSGI environment *(why?)* and does not attempt to express 
anything beyond what is available in the environment dictionary.

The only state maintained in this object is the desired ``charset``, an 
associated errors handler and a ``decode_param_names`` option.

.. _note:

    *Unicode notes*

    When ``charset`` is set, the incoming parameter values will be 
    automatically coerced to unicode objects of the charset encoding.

    When unicode is expected, ``charset`` will be overridden by the the value 
    of the charset parameter set in the Content-Type header, if one was 
    specified by the client.

    The incoming parameter names are not decoded to unicode unless the 
    decode_param_names option is enabled.

The class variable ``defaults`` specifies default values for charset, errors,
and language. These default values can be overridden for the current request 
via the registry *(what's a registry?)*.

The language default value is considered the fallback during i18n 
translations to ensure in odd cases that mixed languages don't occur should 
the language file contain the string but not another language in the accepted 
languages list. The language value only applies when getting a list of 
accepted languages from the HTTP Accept header.

This behavior is duplicated from Aquarium, and may seem strange but is very 
useful. Normally, everything in the code is in "en-us". However, the "en-us" 
translation catalog is usually empty. If the user requests ["en-us", "zh-cn"] 
and a translation isn't found for a string in "en-us", you don't want gettext 
to fallback to "zh-cn". You want it to just use the string itself. Hence, if 
a string isn't found in the language catalog, the string in the source code 
will be used.

All other state is kept in the environment dictionary; this is essential for 
interoperability.

You are free to subclass this object.

Attributes
----------

GET
^^^

A dictionary-like object representing the QUERY_STRING parameters. Always present, possibly empty.

If the same key is present in the query string multiple times, a list of its 
values can be retrieved from the :class:`MultiDict` via the :meth:``getall`` 
method.

Returns a :class:`MultiDict` container or, when charset is set, a :class:`UnicodeMultiDict`.

POST
^^^^

A dictionary-like object representing the ``POST`` body.

Most values are encoded strings, or unicode strings when charset is set. 
There may also be FieldStorage objects representing file uploads. If this is 
not a POST request, or the body is not encoded fields (e.g., an XMLRPC 
request) then this will be empty.

This will consume wsgi.input when first accessed if applicable, but the raw 
version will be put in environ['paste.parsed_formvars'].

Returns a MultiDict container or a UnicodeMultiDict when charset is set.

cookies
^^^^^^^

A dictionary of cookies, keyed by cookie name.

Just a plain dictionary, may be empty but not None.

defaults
^^^^^^^^

.. code-block:: python

    {'errors': 'replace', 
     'decode_param_names': False, 
     'charset': None, 
     'language': 'en-us'}

host
^^^^

The host name, as provided in ``HTTP_HOST`` with a fall-back to :envvar:`SERVER_NAME`

is_xhr
^^^^^^

Returns a boolean if ``X-Requested-With`` is present and is a ``XMLHttpRequest``

languages
^^^^^^^^^

Returns a (possibly empty) list of preferred languages, most preferred first.


params
^^^^^^

A dictionary-like object of keys from ``POST``, ``GET``, ``URL`` dicts

Return a key value from the parameters, they are checked in the following order: POST, GET, URL


Additional methods supported:
-----------------------------

getlist(key)
^^^^^^^^^^^^

Returns a list of all the values by that key, collected from POST, GET, URL dicts

Returns a :class:`MultiDict` container or a :class:`UnicodeMultiDict` when :data:`charset` is set.

urlvars
^^^^^^^

Return any variables matched in the URL (e.g. wsgiorg.routing_args).

Methods
-------

__init__(self, environ)
^^^^^^^^^^^^^^^^^^^^^^^

determine_browser_charset(self)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Determine the encoding as specified by the browser via the Content-Type's ``charset parameter``, if one is set

match_accept(self, mimetypes)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return a list of specified mime-types that the browser's HTTP Accept header allows in the order provided.


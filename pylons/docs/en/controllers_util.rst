.. _controllers_util:

====================
Controller Utilities
====================

.. _controllers_util:

The Request object
==================

.. code-block:: python 

    class Request(WebObRequest):
        """WebOb Request subclass
    
        The WebOb :class:`webob.Request` has no charset, or other defaults. This subclass
        adds defaults, along with several methods for backwards 
        compatibility with paste.wsgiwrappers.WSGIRequest.
    
        """    
        def determine_browser_charset(self):
            """Legacy method to return the
            :attr:`webob.Request.accept_charset`"""
            return self.accept_charset
    
        def languages(self):
            return self.accept_language.best_matches(self.language)
        languages = property(languages)
    
        def match_accept(self, mimetypes):
            return self.accept.first_match(mimetypes)
    
        def signed_cookie(self, name, secret):
            """Extract a signed cookie of ``name`` from the request
        
            The cookie is expected to have been created with
            ``Response.signed_cookie``, and the ``secret`` should be the
            same as the one used to sign it.
        
            Any failure in the signature of the data will result in None
            being returned.
        

The Response object
===================

.. code-block:: python

    class Response(WebObResponse):
        """WebOb Response subclass
    
        The WebOb Response has no default content type, or error defaults.
        This subclass adds defaults, along with several methods for 
        backwards compatibility with paste.wsgiwrappers.WSGIResponse.
    
        """
        content = WebObResponse.body
    
        def determine_charset(self):
            return self.charset
    
        def has_header(self, header):
            return header in self.headers
    
        def get_content(self):
            return self.body
    
        def write(self, content):
            self.body_file.write(content)
    
        def wsgi_response(self):
            return self.status, self.headers, self.body
    
        def signed_cookie(self, name, data, secret=None, **kwargs):
            """Save a signed cookie with ``secret`` signature
        
            Saves a signed cookie of the pickled data. All other keyword
            arguments that ``WebOb.set_cookie`` accepts are usable and
            passed to the WebOb set_cookie method after creating the signed
            cookie value.
        
            """


Using the HTTP Entity Tag cache for browser-side caching
========================================================

.. code-block:: python

    def etag_cache(key=None):
        """Use the HTTP Entity Tag cache for Browser side caching
    
        If a "If-None-Match" header is found, and equivilant to ``key``,
        then a ``304`` HTTP message will be returned with the ETag to tell
        the browser that it should use its current cache of the page.
    
        Otherwise, the ETag header will be added to the response headers.

        Returns ``pylons.response`` for legacy purposes (``pylons.response``
        should be used directly instead).
    
        Suggested use is within a Controller Action like so:
    
        .. code-block:: python
    
            import pylons
        
            class YourController(BaseController):
                def index(self):
                    etag_cache(key=1)
                    return render('/splash.mako')
    
        .. note::
            This works because etag_cache will raise an HTTPNotModified
            exception if the ETag recieved matches the key provided.
    
        """
        pass

``forward``: Forwarding requests to a WSGI application
=======================================================

.. code-block:: python

    def forward(wsgi_app):
        """Forward the request to a WSGI application. Returns its response.
    
        .. code-block:: python
    
            return forward(FileApp('filename'))
    
        """
        pass

``abort``: Aborting the request immediately by returning an HTTP exception
==========================================================================

.. code-block:: python

    def abort(status_code=None, detail="", headers=None, comment=None):
        """Aborts the request immediately by returning an HTTP exception
    
        In the event that the status_code is a 300 series error, the detail
        attribute will be used as the Location header should one not be
        specified in the headers attribute.
    
        """
        pass

``redirect``: Raising a redirect exception to a specified URL
=============================================================

.. code-block:: python

    def redirect(url, code=302):
        """Raises a redirect exception to the specified URL

        Optionally, a code variable may be passed with the status code of
        the redirect, ie::

            redirect(url(controller='home', action='index'), code=303)

        """
        pass


``redirect_to``: Raising a redirect exception to a URL resolved by Routes' :func:`url_for` function
====================================================================================================

.. code-block:: python

    def redirect_to(*args, **kargs):
        """Raises a redirect exception to the URL resolved by Routes'
        url_for function
    
        Optionally, a _code variable may be passed with the status code of
        the redirect, i.e.::

            redirect_to(controller='home', action='index', _code=303)

        """

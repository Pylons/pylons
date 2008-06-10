.. _flickr_search_tutorial:

======================
Flickr search tutorial
======================

Introduction
============

By now you may have seen the `amazing screencast <http://media.rubyonrails.org/video/flickr-rails-ajax.mov>`_ where someone implements a beautiful web interface to `Flickr! <http://www.flickr.com>`_ (an online photo gallery) in under 5 minutes. Well if you haven't seen it yet, you really should do so now. But if you have you would probably be glad to know that this is possible under Pylons too! 

Getting Started 
===============

First install Pylons 0.9.6: 

.. code-block:: bash 

    $ easy_install -U pylons==0.9.6 

Then create your project: 

.. code-block:: bash 

    $ paster create -t pylons FlickrSearch 

add a controller called ``flickr``: 

.. code-block:: bash 

    $ cd FlickrSearch 
    $ paster controller flickr 

Our project is going to use a third party library for Flickr web services. We've picked flickr.py from the `Flickr! API list <http://www.flickr.com/services/api/>`_. All third party libraries you add to a Pylons project can go in the ``lib`` directory so download http://flickrpy.googlecode.com/svn/trunk/flickr.py and put it in ``lib``: 

.. code-block:: bash 

    $ cd flickrsearch/lib 
    $ wget http://flickrpy.googlecode.com/svn/trunk/flickr.py 

Now lets start the server and see what we have: 

.. code-block:: bash 

    $ cd ../../ 
    $ paster serve --reload development.ini 

Note that we have started the server with the ``--reload`` switch. This means any changes we make to code will cause the server to restart if necessary so that you can always test your latest code. 

Flickr API Key 
============== 

To access Flickr! we need a Flickr! API key. You can `get your API key here <http://www.flickr.com/services/api/key.gne>`_ after filling in a very short form. 

Setup the JavaScripts and autohandler 
=====================================

If you look at ``config/middleware.py`` you will see these lines: 

.. code-block:: python 

    javascripts_app = StaticJavascripts() 
    ... 
    app = Cascade([static_app, javascripts_app, app]) 

The ``javascripts_app`` WSGI application maps any requests to ``/javascripts/`` straight to the relevant JavaScript in the WebHelpers package. This means you don't have to manually copy the Pylons JavaScript files to your project and that if you upgrade Pylons, you will automatically be using the latest scripts.

Knowing that we don't need to worry about JavaScript files, edit the file ``templates/base.mako`` with the following content: 

.. code-block:: html+mako 

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" 
    "http://www.w3.org/TR/html4/strict.dtd"> 
    <html> 
    <head> 
    <title>Flickr!</title> 
    ${h.javascript_include_tag('/javascripts/effects.js', builtins=True)} 
    ${h.stylesheet_link_tag('/flickr.css')} 
    </head> 
    <body> 
    ${self.body()} 
    </body> 
    </html> 

If you are interested in learning some of the features of Mako templates have a look at the comprehensive `Mako Documentation <http://www.makotemplates.org/docs/>`_. For now we just need to understand that ``${self.body()}`` is replaced with the child template and that anything in ``${ ... }`` is executed and replaced with the result. In the head of the HTML document, javaScript and stylesheet tags are inserted. 


Write The Controller and Templates 
================================== 

Add the following to your ``controllers/flickr.py``: 

.. code-block:: python 

    import logging 

    from flickrsearch.lib.base import * 
    import flickrsearch.lib.flickr as flickr 

    log = logging.getLogger(__name__) 

    flickr.API_KEY = "Your key here!" 

    class FlickrController(BaseController): 

        def index(self): 
            return render('/flickr.mako') 

        def search(self): 
            photos = flickr.photos_search(tags=request.params['tags'], per_page=24) 
            c.photos = [photo.getURL(size="Small", urlType='source') for photo in photos] 
            return render('/photos.mako') 

It should be pretty straight forward, we import the ``flickr`` API module, set the API_KEY. And define two actions in our controller. The first ``index()`` just renders ``flickr.mako``, the other ``search()`` uses the ``flickr`` API module to select all photos by using the tag from ``request.params['tags']``. ``request.params`` are given to this action by the form from ``templates/flickr.mako`` with a POST method. It then renders the ``templates/photos.mako`` template by calling the Pylons ``render()`` function.

Time to create the two templates. Create ``templates/flickr.mako`` with this content: 

.. code-block:: html+mako 

    <%inherit file="base.mako"/> 
    ${h.form_remote_tag(url=h.url(action="search"), update="photos", 
    complete=h.visual_effect("Blind_down", "photos"), 
    loading=h.update_element_function("spinner", 
    content="loading.."), 
    loaded=h.update_element_function("spinner", content=""))} 
    <div id="spinner"></div> 
    <fieldset> 
    <label for="tags">Tags:</label> 
    ${h.text_field("tags")} 
    ${h.submit("Find")} 
    </fieldset> 
    <div id="photos" style="display:none"></div> 
    ${h.end_form()} 

Create ``templates/photos.mako`` with this content: 

.. code-block:: html+mako 

    % for photo in c.photos: 
    <img class="photo" src="${photo}"> 
    % endfor 

Add Some Style 
==============

Finally we need to add some style to our project so create the stylesheet ``public/flickr.css``. We are going to use the same stylesheet as the Rails example: 

.. code-block:: css 

    body { 
    background-color: #888; 
    font-family: Lucida Grande; 
    font-size: 11px; 
    margin: 25px; 
    } 
    form { 
    margin: 0; 
    margin-bottom: 10px; 
    background-color: #eee; 
    border: 5px solid #333; 
    padding: 25px; 
    } 
    fieldset { 
    border: none; 
    } 
    #spinner { 
    float: right; 
    margin: 10px; 
    } 
    #photos img { 
    border: 1px solid #000; 
    width: 75px; 
    height: 75px; 
    margin: 5px; 
    } 

Quick Recap 
===========

    * Installed a Flickr library 
    * Written a controller with ``index()`` and ``search()`` methods 
    * Written a main template linking to the JavaScripts we need 
    * Created a template fragment to generate HTML to return to the browser via AJAX 
    * Added the necessary CSS 

We are done! OK visit http://127.0.0.1:5000/flickr and check your stopwatch. How long did it take you? 

.. Note:: If you have any problems ensure you have set the ``flickr.API_KEY`` in ``controllers/flickr`` and have a look at the console output from ``paster serve``. If there are any debug URLs logged you can visit those URLs to get an interactive debug prompt and work out where you went wrong! 

Based on `original tutorial for Pylons 0.8 by Nicholas Piel <http://pylonshq.com/project/pylonshq/wiki/RailsFlickrExample>`_ 


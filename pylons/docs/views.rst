.. _views:

=====
Views
=====

About the view
==============

.. image:: ../_static/pylon4.jpg
   :alt: 
   :align: left
   :height: 434
   :width: 368

In the MVC paradigm the *view* manages the presentation of the model. 

The view is the interface the user sees and interacts with. For Web applications, this has historically been an HTML interface. HTML remains the dominant interface for Web apps but new view options are rapidly appearing. 

These include Macromedia Flash, JSON and views expressed in alternate markup languages like XHTML, XML/XSL, WML, and Web services. It is becoming increasingly common for web apps to provide specialised views in the form of a REST API that allows programmatic read/write access to the data model. 

More complex APIs are quite readily implemented via SOAP services, yet another type of view on to the data model.

The growing adoption of RDF, the graph-based representation scheme that underpins the Semantic Web, brings a perspective that is strongly weighted towards machine-readability.

RDF model data is serialized into an undecorated, standardized format that can readily be processed and rendered by client applications of increasing sophistication, such as the MIT `Simile`__ project's "`Fresnel`__", "`Longwell`__" and "`Welkin`__" browser extensions.

.. __: http://simile.mit.edu/
.. __: http://simile.mit.edu/fresnel/
.. __: http://simile.mit.edu/longwell/
.. __: http://simile.mit.edu/welkin/

Handling all of these interfaces in an application is becoming increasingly challenging. One big advantage of MVC is that it makes it easier to create these interfaces and develop a web app that supports many different views and thereby provides a broad range of services.

Typically, no significant processing occurs in the view; it serves only as a means of outputting data and allowing the user (or the application) to act on that data, irrespective of whether it is an online store or an employee list.

.. _templates:

Templates
=========

Template rendering engines are a popular choice for handling the task of view presentation.

In Pylons this functionality is typically implemented using a template rendering engine. Pylons provides pre-configured options for using the `Mako`__, `Genshi`__ and `Jinja`__ template rendering engines.

.. __: http://www.makotemplates.org/
.. __: http://genshi.edgewall.org/
.. __: http://jinja.pocoo.org/

Directly-supported template engines
-----------------------------------

Pylons provides out-of-the-box support for Mako, Genshi and Jinja template engines.

:mod:`pylons.templating`
========================

.. automodule:: pylons.templating


:mod:`pylons.templating` rendering functions
============================================

``Mako``
--------
.. currentmodule:: pylons.templating

.. autofunction:: render_mako


``Genshi``
----------
.. autofunction:: render_genshi


``Jinja``
---------
.. autofunction:: render_jinja


Templating with Mako
====================

Introduction
------------

The template library deals with the *view*, presenting the model. It generates (X)HTML code, CSS and Javascript that is sent to the browser. *(In the examples for this section, the project root is ``myapp``.)* 

Static vs. dynamic
^^^^^^^^^^^^^^^^^^

Templates to generate dynamic web content are stored in `myapp/templates`, static files are stored in `myapp/public`.

Both are served from the server root, **if there is a name conflict the static files will be served in preference**

Making templates unicode safe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit :file:`config/environment.py` and add these lines just after `tmpl_options = {}` is declared,

.. code-block:: python

    tmpl_options['mako.input_encoding'] = 'UTF-8'
    tmpl_options['mako.output_encoding'] = 'UTF-8'
    tmpl_options['mako.default_filters'] = ['decode.utf8']


then change the final `return` statement in the same file so that it reads,

.. code-block:: python

    return pylons.config.Config(tmpl_options, map, paths,
        request_settings = dict(charset = 'utf-8', error = 'replace'))

Also, ensure that all templates begin with the line:

.. code-block:: html+mako

    # -*- coding: utf-8 -*-


Making a template hierarchy
---------------------------

Create a base template
^^^^^^^^^^^^^^^^^^^^^^

In `myapp/templates` create a file named `base.mako` and edit it to appear as follows:

.. code-block:: html+mako

    # -*- coding: utf-8 -*-
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
      <head>
        ${self.head_tags()}
      </head>
      <body>
        ${self.body()}
      </body>
    </html>

A base template such as the very basic one above can be used for all pages rendered by Mako. This is useful for giving a consistent look to the application. 

* Expressions wrapped in `${...}` are evaluated by Mako and returned as text 
* `${` and `}` may span several lines but the closing brace should not be on a line by itself (or Mako throws an error)
* Functions that are part of the `self` namespace are defined in the Mako templates

Create child templates
^^^^^^^^^^^^^^^^^^^^^^

Create another file in `myapp/templates` called `my_action.mako` and edit it to appear as follows:

.. code-block:: html+mako

    # -*- coding: utf-8 -*-
    <%inherit file="/base.mako" />

    <%def name="head_tags()">
      <!-- add some head tags here -->
    </%def>

    <h1>My Controller</h1>

    <p>Lorem ipsum dolor ...</p>

This file  define the functions called by `base.mako`. 

* The `inherit` tag specifies a parent file to pass program flow to
* Mako defines functions with `<%def name="function_name()">...</%def>`, the contents of the tag are returned
* Anything left after the Mako tags are parsed out is automatically put into the `body()` function

A consistent feel to an application can be more readily achieved if all application pages refer back to single file (in this case `base.mako`)..

Rendering a Mako template from a controller
-------------------------------------------

In the controller action, use the following as a `return()` value,

.. code-block:: python

    return render_response('/my_action.mako')


Now run the action, usually by visiting something like ``http://localhost:5000/my_controller/my_action`` in a browser (if Pylons is running)

Selecting 'View Source' in the browser should reveal the following output:

.. code-block:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
      <head>
      <!-- add some head tags here -->
      </head>
      <body>

    <h1>My Controller</h1>

    <p>Lorem ipsum dolor ...</p>

      </body>
    </html>

Passing variables to Mako from the controller
---------------------------------------------

Add the following to the controller action just before the `return` line,

.. code-block:: python

    c.title = 'Mr Jones lives!'

and now in `myapp/template/my_action.mako` add the following in place of `<!-- add some head tags here -->`,

.. code-block:: html+mako

    <title>${c.title}</title>

Now, when run, the browser window title should read 'Mr Jones lives!'

* The `c` dictionary is passed to Mako from the controller

``c`` is an import synonym for ``tmpl_context``, an instance of either the :class:`AttribSafeContextObj` class or its parent :class:`ContextObj` class. Accessing a nonexistent attribute of a :class:ContextObj raises an ``AttributeError`` exception whereas an instance of :class:`AttribSafeContextObj` returns an empty string and does not cause an exception to be raised. This more tolerant option can be used to avoid templates becoming cluttered with repetitive screening tests for the existence of attributes. It can also result in a degree of puzzlement on those occasions when this behavior is not expected. It can be disabled by setting ``config['pylons.strict_c'] = True`` in the project's ``config/environment.py``.

.. warning:: The templating engine for the Jinja template language requires ``strict_c`` to be set to `True`. This variable affects *all* of the loaded templating engines so any Mako templates that contain tests of the form: ``% if c.some_attrib is not UNDEFINED:`` will cause AttributeError exceptions.

Using Webhelpers
----------------

The Webhelper functions are available in Mako templates under the `h` object. Some useful ones are,

* `h.stylesheet_link_tag('base')` - This returns a link tag to a static stylesheet named `base.css` in `myapp/public/stylesheets`
* `h.javascript_include_tag('base')` - This return a script tag to a static javascript file named `base.js` in `myapp/public/scripts`

The Pylons Cookbook article `Routes for people in a hurry`__ describes how to generate internal application URIs using Webhelpers

.. __: http://wiki.pylonshq.com/display/pylonscookbook/Routes+for+people+in+a+hurry

The rest of the webhelpers are documented in `Webhelpers documentation <http://pylonshq.com/WebHelpers/module-index.html>`_. 

Python in Mako
--------------

Arbitrary Python code can be included in Mako by enclosing it in `<%` and `%>`. Note that the `template context <http://www.makotemplates.org/docs/runtime.html#runtime_context>`_ is used to actually output the text from a Python block in a Mako template.

.. code-block:: html+mako

    <%
    c.mr_jones.age = datetime.date.year() - c.mr_jones.birthday.year 
    if c.mr_jones.age > 12:
      context.write('<p>Sorry Mr Jones, you are too old for Pandas Palace!</p>')
    %>

Pythons flow control elements (`for`, `while`, `if` etc.) can be used reasonably directly with slight modification,

.. code-block:: html+mako

    % if c.mr_jones.age > 12:
    <p>Sorry Mr Jones, you are too old for Pandas Palace!</p>
    <p>Try Barry's Bingo instead</p>
    % endif

* Flow is opened with `% <flow_element>` and must be 'closed' with `% end<flow_element>`

.. seealso::

    The `Mako documentation <http://www.makotemplates.org/docs/>`_
        Reasonably straightforward to follow

    See the `official Pylons docs on unicode support <http://docs.pythonweb.org/display/pylonsdocs/Internationalization%2C+Localization+and+Unicode>`_ 
        Provides more help on making your application more worldly.


Switching the Default Template Engine 
===================================== 

In Pylons, customization is not just allowed but actively encouraged. It's quite easy to change the default engine from Mako to your choice. Let's make Genshi the default template engine. 

Edit ``yourproject/config/environment.py`` and change the ``template_engine`` argument passed to `config.init_app`: 

.. code-block:: python 

    config.init_app(global_conf, app_conf, package='yourproject', 
    template_engine='kid', paths=paths) 


This swaps Mako out and uses Kid, making Kid the new default template engine. The above ``index`` method no longer needs to specify 'kid' now when rendering a template. The existing templates directory will be used, and you'll need to create the ``__init__.py`` file before adding Kid templates. Current template engine's that can be swapped in this manner are kid, mako, and genshi. 

.. Note::  For more details on the config object, check out the `extensive Config docs <http://pylonshq.com/docs/class-pylons.config.Config.html>`_ from the Pylons Module API. 


.. _using_other_template_languages:

Using other template languages
==============================

.. warning:: Prior to 0.9.7, all templating was handled through a layer called 'Buffet'. This layer frequently made customization of the template engine difficult as any customization required additional plugin modules being installed. Pylons 0.9.7 now deprecates use of the Buffet plug-in layer.

Example: adding the Brevé template language
-------------------------------------------

Pylons requires two things of a template language: a template loader function and a template render function. If the template engin does not provide off-the-shelf integration with Pylons, this integration can be added fairly simply by creating an interface module in the project's ``lib`` directory.

In this example, the interface module is called ``template``. The module is  defined in ``myapp/lib/template.py`` and makes available a template loader class: :class:`PathLoader` plus a template render function: :func:`render_breve`.

``myapp/lib/template.py``
-------------------------

Imports
^^^^^^^

The module imports ``pylons.config`` and :func:`pylons_globals` from ``pylons.templating``,  providing the template render function with the necessary access to config variables. Imports from ``breve`` provide access to Brevé's :class:`Template` template-handling class and to a set of tags supplied as args to the Brevé :class:`Template` :func:`render` function.

.. code-block:: python

    # -*- coding: utf-8 -*-
	
    from pylons.templating import pylons_globals
    from pylons import config
    from breve import Template
    from breve.tags.html import tags

The template loader
^^^^^^^^^^^^^^^^^^^^

Brevé's own :class:`PathLoader` class is pressed into service as the template loader. At runtime it will be bound to the environment in ``pylons.app_globals``, ready for subsequent retrieval and call by the template rendering function: 

.. code-block:: python

    class PathLoader ( object ):
        __slots__ = [ 'paths' ]
    
        def __init__ ( self, *paths ):
            self.paths = paths
    
        def stat ( self, template, root ):
            import os
            for p in self.paths:
                f = os.path.join ( root, p, template )
                if os.path.isfile ( f ):
                    timestamp = long ( os.stat ( f ).st_mtime )
                    uid = f
                    return uid, timestamp
            raise OSError, 'No such file or directory %s' % template
    
        def load ( self, uid ):
    
            return file ( uid, 'U' ).read ( )

The template renderer
^^^^^^^^^^^^^^^^^^^^^

The template renderer function uses the imported :func:`pylons_globals` to retrieve configuration variables, including ``breve_loader``, the Brevé template loader function previously bound to config in ``environment.py`` (above). The loader will load the appropriate template file when called by the template renderer.

.. code-block:: python

    def render_breve(template_name, extra_vars=None):
        # Pull in extra vars if needed

        globs = extra_vars or {}

        # Second, get the globals
        globs.update(pylons_globals())

        # Retrieve the Breve template loader from config 
        loader = config['pylons.app_globals'].breve_loader

        # Instantiate a Breve template, supplying (default)
        # tags and specifying a Breve template directory
        # relative to the project root
        template = Template ( tags, root = "brevetemplates" )

        return template.render(template_name, loader=loader, vars=globs)

Template caching
^^^^^^^^^^^^^^^^

Breve handles template caching internally. Had that not been the case, a template caching facility :func:`cached_template` can be imported from ``pylons.templating``:

.. code-block:: python

    from pylons.templating import pylons_globals

and used to create a cacheing wrapper around the template renderer:

.. code-block:: python

    def render_breve(template_name, extra_vars=None, cache_key=None, 
                    cache_type=None, cache_expire=None):
        """Render a template with Breve
    
        Accepts the cache options ``cache_key``, ``cache_type``, and
        ``cache_expire``.
    
        """    
        # Create a render callable for the cache function
        def render_template():
            # Pull in extra vars if needed
            globs = extra_vars or {}
        
            # Second, get the globals
            globs.update(pylons_globals())

            # Retrieve the Breve template loader from config 
            loader = config['pylons.app_globals'].breve_loader
            
            # Instantiate a Breve template, supplying (default)
            # tags and specifying a Breve template directory
            # relative to the project root
            template = Template ( tags, root = "brevetemplates" )
            
            return template.render(template_name, loader=loader, vars=globs)
    
        return cached_template(template_name, 
                               render_template, 
                               cache_key=cache_key,
                               cache_type=cache_type, 
                               cache_expire=cache_expire)


Template engine configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The template loader import is added to the import statements in ``config/environment.py``:

.. code-block:: python

    from myapp.lib.template import PathLoader

The requisite template initialisation and configuration operations are added at the relevant point. The required operations are: iterating over any options given in ``development.ini``, instantiating the template loader with an appropriate template directory, binding the template loader instance to the environment and finally adding the template engine to the config dictionary.

.. code-block:: python

    def load_environment(global_conf, app_conf):

        [ ... ]

        # CONFIGURATION OPTIONS HERE (note: all config options will override
        # any Pylons config options)

        # Setup Breve Template Engine
        # Retrieve breve.* options from config
        breve_options = dict((k,v) for k,v in app_conf.iteritems() 
                                     if k.startswith('breve'))

        # Create the Breve TemplateLoader
        config['pylons.app_globals'].breve_loader = \
            PathLoader(os.path.join(root, 'brevetemplates'))
        # Add the Breve template engine to the config
        config.add_template_engine(
                'breve', 'bel.brevetemplates', breve_options)

Calling the template renderer from a controller action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Typical usage in a controller action:

.. code-block:: python

    class TestingController(BaseController):

        def index(self):
            from myapp.lib.template import render_breve
            c.title = u'Title here'
            c.content = loremipsum
            return render_breve('test')

All the same Pylons variables are made accessible to template engine plug-ins. The variables ``c``, ``h``, ``g``, ``session``, and ``request`` are available in any chosen template language. This also makes it easier to switch between and change template languages without extensive refactoring of controller actions.

Template files
^^^^^^^^^^^^^^

With the above configuration, Breve will search for template in myapp/brevetemplates and will search for a matching filename with a ``.b`` extension.

``myapp/brevetemplates/test.b``

.. code-block:: python

    html [
        head [ title [ c.title ] ],
        body [ h1 [ c.title ],
                div [ p [ c.content ] ] ] 
        ]


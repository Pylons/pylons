.. _views:

=====
Views
=====

About the view
==============

.. image:: _static/pylon4.jpg
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

Template rendering engines are a popular choice for handling view presentation.

In Pylons this functionality is typically implemented using a template rendering engine. Pylons provides pre-configured options for using the Mako and Genshi template rendering engines.


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

The template library deals with the *view*, presenting the model. It generates (X)HTML code, CSS and Javascript that is sent to the browser.

Static vs. dynamic
^^^^^^^^^^^^^^^^^^

Templates to generate dynamic web content are stored in `YOURPROJ/templates`, static files are stored in `YOURPROJ/public`.

Both are served from the server root, **if there is a name conflict the static files will be served in preference**

Install and setup Mako
----------------------

.. warning:: Is this step still required for Pylons 0.9.6+>

Next open :file:`config/middleware.py` and add `template_engine='mako'` to :data:`config.init_app` so that it reads,

.. code-block:: python

    config.init_app(global_conf, app_conf, package='myapp', template_engine='mako')


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

Also, ensure that all templates you create begin with the line:

.. code-block:: html+mako

    # -*- coding: utf-8 -*-


Making a template hierarchy
---------------------------

Create a base template
^^^^^^^^^^^^^^^^^^^^^^

In `YOURPROJ/templates` create a file named `base.mako` and edit it to appear as follows:

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

We can use a base template such as the very basic one above for all pages rendered by Mako. This is useful for giving a consistent look to the application. 

* Expressions wrapped in `${...}` are evaluated by Mako and returned as text 
* `${` and `}` may span several lines but the closing brace should not be on a line by itself (or Mako throws an error)
* Functions that are part of the `self` namespace are defined in the Mako templates

Create child templates
^^^^^^^^^^^^^^^^^^^^^^

Create another file in `YOURPROJ/templates` called `my_action.mako` and edit it to appear as follows:

.. code-block:: html+mako

    # -*- coding: utf-8 -*-
    <%inherit file="/base.mako" />

    <%def name="head_tags()">
      <!-- add some head tags here -->
    </%def>

    <h1>My Controller</h1>

    <p>Lorem ipsum dolor ...</p>

Here we define the functions called by `base.mako`. 

* The `inherit` tag specifies a parent file to pass program flow to
* Mako defines functions with `<%def name="function_name()">...</%def>`, the contents of the tag are returned
* Anything left after the Mako tags are parsed out is automatically put into the `body()` function

If all your application pages refer back to single file (in this case `base.mako`), you can keep a consistent feel to your application.

Rendering a Mako template from a controller
-------------------------------------------

In your controller action, use the following as a `return()` value,

.. code-block:: python

    return render_response('/my_action.mako')


Now run the action, usually by visiting something like [http://localhost:5000/my_controller/my_action] in your browser (if Pylons is running)

If you do 'View Source' in your browser the output should be the following,

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

Add the following to your controller action just before the `return` line,

.. code-block:: python

    c.title = 'Mr Jones lives!'

and now in `YOURPROJ/template/my_action.mako` add the following in place of `<!-- add some head tags here -->`,

.. code-block:: html+mako

    <title>${c.title}</title>

Now when run the browser window title should read 'Mr Jones lives!'

* The `c` dictionary is passed to Mako from the controller

Using Webhelpers
----------------

The Webhelper functions are available in Mako templates under the `h` object. Some useful ones are,

* `h.stylesheet_link_tag('base')` - This returns a link tag to a static stylesheet named `base.css` in `myapp/public/stylesheets`
* `h.javascript_include_tag('base')` - This return a script tag to a static javascript file named `base.js` in `myapp/public/scripts`

[Routes for people in a hurry] describes how you should generate internal application URIs using Webhelpers

The rest of the webhelpers are documented in `Webhelpers documentation <http://pylonshq.com/WebHelpers/module-index.html>`_. 

Python in Mako
--------------

You can include arbitrary Python code in Mako by enclosing it in `<%` and `%>`. Note that to actually output the text from a Python block in your Mako template, you need to write to the `template context <http://www.makotemplates.org/docs/runtime.html#runtime_context>`_.

.. code-block:: html+mako

    <%
    c.mr_jones.age = datetime.date.year() - c.mr_jones.birthday.year 
    if c.mr_jones.age > 12:
      context.write('<p>Sorry Mr Jones, you are too old for Pandas Palace!</p>')
    %>

We can also use Pythons flow control elements (`for`, `while`, `if` etc.) more directly with slight modification,

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


.. _using_other_template_languages:

Using other template languages
==============================

Template Language Plugins 
------------------------- 

Pylons supports a variety of template languages in addition to Mako through the use of template engine plug-ins. This can be useful both for migrating web applications to Pylons, or in cases where you just would rather prefer some other templating solution. 

Template language plug-ins can be installed rather easily using setuptools. A current list of template engine plug-ins is at the `Buffet <http://projects.dowski.com/projects/buffet>`_ website. 

Once you have installed one of these, using the new template language within Pylons is quite easy. As Pylons does not come pre-configured with this in mind, you will need to do a little more work yourself depending on which template language you're using. 


Example: Using Kid with Pylons 
------------------------------ 

If you didn't select the ``kid`` optional extra package when you installed Pylons (described on the `install page <Installing+Pylons>`_) you will need to install the appropriate Buffet plugin. In the case of Kid, this is called TurboKid and can be installed as follows: 

.. code-block:: bash 

    $ easy_install TurboKid 

To use Kid with Pylons, first we must setup a new template directory for the Kid templates. 

First, create a directory in ``yourproject`` called ``kidtemplates`` and add a controller: 

.. code-block:: bash 

    $ cd yourproject 
    $ mkdir yourproject/kidtemplates 
    $ paster controller kid 

You will now have a kid.py controller in your controllers directory. First, we will need to add Kid to the available template engines. 

Edit ``yourproject/config/environment.py`` add to the bottom of the ``load_environment`` function: 

.. code-block:: python 

    kidopts = {'kid.assume_encoding':'utf-8', 'kid.encoding':'utf-8'} 
    config.add_template_engine('kid', 'yourproject.kidtemplates', kidopts) 

Edit the KidController class so it looks like this: 

.. code-block:: python 

    class KidController(BaseController): 
        def index(self): 
            c.title = "Your Page" 
            c.message = 'hi' 
            return render_response('kid', 'test') 

Make sure to change ``yourproject.kidtemplates`` to reflect what your project is actually called. The 
first argument to ``render`` or ``render_response`` can be the template engine to use, while the second non-keyword argument is the template. If you don't specify a template engine, it will drop back to the default (Mako, unless you change the default). 

Now let's add the Kid template to render, create the file ``yourproject/kidtemplates/test.kid`` with 
the following content: 

.. code-block:: html+genshi 

    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"> 
        <head> 
            <title py:content="c.title">title</title> 
        </head> 
        <body> 
            <p py:content="c.message">message</p> 
            <p>You made it to the following url: ${h.url_for()}</p> 
        </body> 
    </html> 

Since the template plug-ins currently expect paths to act as module imports, you will also need to create 
a ``__init__.py`` file inside ``yourproject/kidtemplates``. 

Loading ``/kid`` will now return the Kid template that you have created. 

Notice that all the same Pylons variables are made accessible to template engine plug-ins. You will have c, h, g, 
session, and request available in any template language you choose to use. This also makes it easier to switch 
later to Mako or a different template language without having to update your controller action. 


Switching the Default Template Engine 
------------------------------------- 

In Pylons, customization is not just allowed but actively encouraged. It's quite easy to change the default engine from Mako to your choice. Let's make Kid the default template engine. 

Edit ``yourproject/config/environment.py`` and change the ``template_engine`` argument passed to `config.init_app`: 

.. code-block:: python 

    config.init_app(global_conf, app_conf, package='yourproject', 
    template_engine='kid', paths=paths) 


This swaps Mako out and uses Kid, making Kid the new default template engine. The above ``index`` method no longer needs to specify 'kid' now when rendering a template. The existing templates directory will be used, and you'll need to create the ``__init__.py`` file before adding Kid templates. Current template engine's that can be swapped in this manner are kid, mako, and genshi. 

.. Note::  For more details on the config object, check out the `extensive Config docs <http://pylonshq.com/docs/class-pylons.config.Config.html>`_ from the Pylons Module API. 


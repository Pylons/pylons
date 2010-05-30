.. _views:

=====
Views
=====


.. image:: _static/pylon4.jpg
   :alt: 
   :align: left
   :height: 434px
   :width: 368px

In the MVC paradigm the *view* manages the presentation of the model. 

The view is the interface the user sees and interacts with. For Web applications, this has historically been an HTML interface. HTML remains the dominant interface for Web apps but new view options are rapidly appearing. 

These include Macromedia Flash, JSON and views expressed in alternate markup languages like XHTML, XML/XSL, WML, and Web services. It is becoming increasingly common for web apps to provide specialised views in the form of a REST API that allows programmatic read/write access to the data model. 

More complex APIs are quite readily implemented via SOAP services, yet another type of view on to the data model.

The growing adoption of RDF, the graph-based representation scheme that underpins the Semantic Web, brings a perspective that is strongly weighted towards machine-readability.

.. NOTE: As much as I love RDF I think the following paragraph is too verbose for our intro docs, maybe we can put this elsewhere -pjenvey
.. RDF model data is serialized into an undecorated, standardized format that can readily be processed and rendered by client applications of increasing sophistication, such as the MIT `Simile`__ project's "`Fresnel`__", "`Longwell`__" and "`Welkin`__" browser extensions.

.. .. __: http://simile.mit.edu/
.. .. __: http://simile.mit.edu/fresnel/
.. .. __: http://simile.mit.edu/longwell/
.. .. __: http://simile.mit.edu/welkin/

Handling all of these interfaces in an application is becoming increasingly challenging. One big advantage of MVC is that it makes it easier to create these interfaces and develop a web app that supports many different views and thereby provides a broad range of services.

Typically, no significant processing occurs in the view; it serves only as a means of outputting data and allowing the user (or the application) to act on that data, irrespective of whether it is an online store or an employee list.

.. _templates:

*********
Templates
*********

Template rendering engines are a popular choice for handling the task of view presentation.

To return a processed template, it must be rendered and returned by the controller::
    
    from helloworld.lib.base import BaseController, render

    class HelloController(BaseController):
        def sample(self):
            return render('/sample.mako')

Using the default Mako template engine, this will cause Mako to look in the :file:`helloworld/templates` directory (assuming the project is called 'helloworld') for a template filed called :file:`sample.mako`.

The :func:`render` function used here is actually an alias defined in your projects' :file:`base.py` for Pylons' :func:`~pylons.templating.render_mako` function.


Directly-supported template engines
===================================

Pylons provides pre-configured options for using the `Mako`__, `Genshi`__ and `Jinja2`__ template rendering engines. They are setup automatically during the creation of a new Pylons project, or can be added later manually.


.. __: http://www.makotemplates.org/
.. __: http://genshi.edgewall.org/
.. __: http://jinja.pocoo.org/


******************************
Passing Variables to Templates
******************************

To pass objects to templates, the standard Pylons method is to attach them to the :term:`tmpl_context` (aliased as `c` in controllers and templates, by default) object in the :ref:`controllers`::

    import logging

    from pylons import request, response, session, tmpl_context as c, url
    from pylons.controllers.util import abort, redirect

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)
    
    class HelloController(BaseController):

        def index(self):
            c.name = "Fred Smith"
            return render('/sample.mako')

Using the variable in the template:

.. code-block:: html+mako
    
    Hi there ${c.name}!

Strict vs Attribute-Safe tmpl_context objects
=============================================

The :term:`tmpl_context` object is created at the beginning of every request, and by default is an instance of the :class:`~pylons.util.AttribSafeContextObj` class, which is an Attribute-Safe object. This means that accessing attributes on it that do **not** exist will return an empty string **instead** of raising an :exc:`AttributeError` error.

This can be convenient for use in templates since it can act as a default:

.. code-block:: html+mako
    
    Hi there ${c.name}

That will work when `c.name` has not been set, and is a bit shorter than what would be needed with the strict :class:`~pylons.util.ContextObj` context object.

Switching to the strict version of the :term:`tmpl_context` object can be done in the :file:`config/environment.py` by adding (after the config.init_app)::
    
    config['pylons.strict_c'] = True


.. _template-globals:

**************************
Default Template Variables
**************************

By default, all templates have a set of variables present in them to make it easier to get to common objects. The full list of available names present in the templates global scope:

- :term:`c` -- Template context object (Alias for :term:`tmpl_context`)
- :term:`tmpl_context` -- Template context object
- :data:`config` -- Pylons :class:`~pylons.configuration.PylonsConfig`
  object (acts as a dict)
- :term:`g` -- Project application globals object (Alias for :term:`app_globals`)
- :term:`app_globals` -- Project application globals object
- :term:`h` -- Project helpers module reference
- :data:`request` -- Pylons :class:`~pylons.controllers.util.Request`
  object for this request
- :data:`response` -- Pylons :class:`~pylons.controllers.util.Response`
  object for this request
- :class:`session` -- Pylons session object (unless Sessions are
  removed)
- :class:`translator` -- Gettext translator object configured for
  current locale
- :func:`ungettext` -- Unicode capable version of gettext's ngettext
  function (handles plural translations)
- :func:`_` -- Unicode capable gettext translate function
- :func:`N_` -- gettext no-op function to mark a string for
  translation, but doesn't actually translate
- :class:`url <routes.util.URLGenerator>` -- An instance of the :class:`routes.util.URLGenerator` configured for this request.


****************************
Configuring Template Engines
****************************

A new Pylons project comes with the template engine setup inside the projects' :file:`config/environment.py` file. This section creates the Mako template lookup object and attaches it to the :term:`app_globals` object, for use by the template rendering function.

.. code-block:: python

    # these imports are at the top
    from mako.lookup import TemplateLookup
    from pylons.error import handle_mako_error
    
    # this section is inside the load_environment function
    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])


Using Multiple Template Engines
===============================

Since template engines are configured in the :file:`config/environment.py` section, then used by render functions, it's trivial to setup additional template engines, or even differently configured versions of a single template engine. However, custom render functions will frequently be needed to utilize the additional template engine objects.

Example of additional Mako template loader for a different templates directory for admins, which falls back to the normal templates directory::
    
    # Add the additional path for the admin template
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')],
                 admintemplates=[os.path.join(root, 'admintemplates'),
                                 os.path.join(root, 'templates')])
    
    config['pylons.app_globals'].mako_admin_lookup = TemplateLookup(
        directories=paths['admin_templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'admintemplates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

That adds the additional template lookup instance, next a :ref:`custom render function <custom-render>` is needed that utilizes it::
    
    from pylons.templating import cached_template, pylons_globals
    
    def render_mako_admin(template_name, extra_vars=None, cache_key=None, 
                          cache_type=None, cache_expire=None):
        # Create a render callable for the cache function
        def render_template():
            # Pull in extra vars if needed
            globs = extra_vars or {}

            # Second, get the globals
            globs.update(pylons_globals())

            # Grab a template reference
            template = globs['app_globals'].mako_admin_lookup.get_template(template_name)

            return template.render(**globs)

        return cached_template(template_name, render_template, cache_key=cache_key,
                               cache_type=cache_type, cache_expire=cache_expire)

The only change from the :func:`~pylons.templating.render_mako` function that comes with Pylons is to use the `mako_admin_lookup` rather than the `mako_lookup` that is used by default.


.. _custom-render:

*******************************
Custom :func:`render` functions
*******************************

Writing custom render functions can be used to access specific features in a template engine, such as Genshi, that go beyond the default :func:`~pylons.templating.render_genshi` functionality or to add support for additional template engines.

Two helper functions for use with the render function are provided to make it easier to include the common Pylons globals that are useful in a template in addition to enabling easy use of cache capabilities. The :func:`pylons_globals` and :func:`cached_template` functions can be used if desired.

Generally, the custom render function should reside in the project's
``lib/`` directory, probably in :file:`base.py`.

Here's a sample Genshi render function as it would look in a project's
``lib/base.py`` that doesn't fully render the result to a string, and
rather than use :data:`c` assumes that a dict is passed in to be used
in the templates global namespace. It also returns a Genshi stream
instead the rendered string.

.. code-block:: python
    
    from pylons.templating import pylons_globals
    
    def render(template_name, tmpl_vars):
        # First, get the globals
        globs = pylons_globals()

        # Update the passed in vars with the globals
        tmpl_vars.update(globs)
        
        # Grab a template reference
        template = globs['app_globals'].genshi_loader.load(template_name)
        
        # Render the template
        return template.generate(**tmpl_vars)

Using the :func:`~pylons.templating.pylons_globals` function also makes it easy to get to the :term:`app_globals` object which is where the template engine was attached in :file:`config/environment.py`.

.. versionchanged:: 0.9.7
    Prior to 0.9.7, all templating was handled through a layer called 'Buffet'. This layer frequently made customization of the template engine difficult as any customization required additional plugin modules being installed. Pylons 0.9.7 now deprecates use of the Buffet plug-in layer.

.. seealso::
    :mod:`pylons.templating` - Pylons templating API


********************
Templating with Mako
********************

Introduction
============

The template library deals with the *view*, presenting the model. It generates (X)HTML code, CSS and Javascript that is sent to the browser. *(In the examples for this section, the project root is ``myapp``.)* 

Static vs. dynamic
------------------

Templates to generate dynamic web content are stored in `myapp/templates`, static files are stored in `myapp/public`.

Both are served from the server root, **if there is a name conflict the static files will be served in preference**

Making a template hierarchy
===========================

Create a base template
----------------------

In `myapp/templates` create a file named `base.mako` and edit it to appear as follows:

.. code-block:: html+mako

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
----------------------

Create another file in `myapp/templates` called `my_action.mako` and edit it to appear as follows:

.. code-block:: html+mako

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

Check that it works
-------------------

In the controller action, use the following as a `return()` value,

.. code-block:: python

    return render('/my_action.mako')


Now run the action, usually by visiting something like ``http://localhost:5000/my_controller/my_action`` in a browser. Selecting 'View Source' in the browser should reveal the following output:

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

.. seealso::

    The `Mako documentation <http://www.makotemplates.org/docs/>`_
        Reasonably straightforward to follow

    See the :ref:`i18n` 
        Provides more help on making your application more worldly.


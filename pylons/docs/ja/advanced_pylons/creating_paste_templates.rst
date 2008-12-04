.. _creating_paste_templates:

========================
Creating Paste templates
========================

Introduction
============

`Python Paste <http://pythonpaste.org/>`_ is an extremely powerful package that isn't just about WSGI middleware. The related document :ref:`entry_points_and_plugins` demonstrates how to use entry_points to create simple plugins. This document describes how to write just such a plugin for use Paste's project template creation facility and how to add a command to Paste's ``paster`` script.

The example task is to create a template for an imaginary content management system. The template is going to produce a project directory structure for a Python package, so we need to be able to specify a package name. 

Creating The Directory Structure and Templates
==============================================

The directory structure for the new project needs to look like this:

.. code-block:: text

    - default_project
        - +package+
            - __init__.py
            - static
                - layout
                - region
                - renderer
            - service
                - layout
                    - __init__.py
                - region
                    - __init__.py
                - renderer
                    - __init__.py
        - setup.py_tmpl
        - setup.cfg_tmpl
        - development.ini_tmpl
        - README.txt_tmpl
        - ez_setup.py

Of course, the actual project's directory structure might look very different. In fact the ``paster create`` command can even be used to generate directory structures which *aren't* project templates --- although this wasn't what it was designed for.

When the ``paster create`` command is run, any directories with ``+package+`` in their name will have that portion of the name replaced by a simplified package name and likewise any directories with ``+egg+`` in their name will have that portion replaced by the name of the egg directory, although we don't make use of that feature in this example.

All of the files with ``_tmpl`` at the end of their filenames are treated as templates and will have the variables they contain replaced automatically. All other files will remain unchanged.

.. note:: The small templating language used with ``paster create`` in files ending in ``_tmpl`` is described in detail in the `Paste util module documentation <http://pythonpaste.org/module-paste.util.template.html>`_

When specifying a package name it can include capitalisation and ``_`` characters but it should be borne in mind that the actual name of the package will be the *lowercase* package name with the ``_`` characters removed. If the package name contains an ``_``, the egg name will contain a ``_`` character so occasionally the ``+egg+`` name is different to the ``+package+`` name. 

To avoid difficulty always recommend to users that they stick with package names that contain no ``_`` characters so that the names remain unique when made lowercase.

Implementing the Code
=====================

Now that the directory structure has been defined, the next step is to implement the commands that will convert this to a ready-to-run project. The template creation commands are implemented by a class derived from ``paste.script.templates.Template``. This is how our example appears:

.. code-block:: python

    from paste.script.templates import Template, var

    vars = [
        var('version', 'Version (like 0.1)'),
        var('description', 'One-line description of the package'),
        var('long_description', 'Multi-line description (in reST)'),
        var('keywords', 'Space-separated keywords/tags'),
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('url', 'URL of homepage'),
        var('license_name', 'License name'),
        var('zip_safe', 'True/False: if the package can be distributed as a .zip file',
            default=False),
    ]
        
    class ArtProjectTemplate(Template):
        _template_dir = 'templates/default_project'
        summary = 'Art project template'
        vars = vars

The ``vars`` arguments can all be set at run time and will be available to be used as (in this instance) Cheetah template variables in the files which end ``_tmpl``. For example the ``setup.py_tmpl`` file for the ``default_project`` might look like this:

.. code-block:: html+mako

    from setuptools import setup, find_packages

    version = ${repr(version)|"0.0"}

    setup(name=${repr(project)},
        version=version,
        description="${description|nothing}",
        long_description="""\
        ${long_description|nothing}""",
        classifiers=[], 
        keywords=${repr(keywords)|empty},
        author=${repr(author)|empty},
        author_email=${repr(author_email)|empty},
        url=${repr(url)|empty},
        license=${repr(license_name)|empty},
        packages=find_packages(exclude=['ez_setup']),
        include_package_data=True,
        zip_safe=${repr(bool(zip_safe))|False},
        install_requires=[
          # Extra requirements go here # 
        ],
        entry_points="""
            [paste.app_factory]
            main=${package}:make_app
        """,
    )


.. note: The list of available classifier strings can be obtained from: ``http://www.python.org/pypi?%3Aaction=list_classifiers``

Note how the variables specified in ``vars`` earlier are used to generate the actual ``setup.py`` file.

In order to use the new templates they must be hooked up to the ``paster create`` command by means of an entry point. In the ``setup.py`` file of the project (in which created the project template is going to be stored) we need to add the following:

.. code-block:: python

    entry_points="""
        [paste.paster_create_template]
        art_project=art.entry.template:ArtProjectTemplate
    """,

We also need to add ``PasteScript>=1.3`` to the ``install_requires`` line. 

.. code-block:: python

    install_requires=["PasteScript>=1.3"],

We just need to install the entry points now by running:

.. code-block:: bash

    python setup.py develop

We should now be able to see a list of available templates with this command:

.. code-block:: bash

    $ paster create --list-templates


.. note:: Windows users will need to add their Python scripts directory to their path or enter the full version of the command, similar to this:

	.. code-block:: bash
	  
		C:\Python24\Scripts\paster.exe create --list-templates
        
You should see the following:

.. code-block:: text

    Available templates:
    art_project:              Art project template
    basic_package:            A basic setuptools-enabled package


There may be other projects too. 


Troubleshooting
===============

If the Art entries don't show up, check whether it is possible to import the ``template.py`` file because any errors are simply ignored by the paster create command rather than output as a warning.

If the code is correct, the issue might be that the entry points data hasn't been updated. Examine the Python ``site-packages`` directory and delete the ``Art.egg-link`` files, any ``Art*.egg`` files or directories and remove any entries for art from ``easy_install.pth`` (replacing ``Art`` with the name chosen for the project of course). Then re-run ``python setup.py develop`` to install the correct information.

If problems are still evident, then running the following code will print out a list of all entry points. It might help track the problem down:

.. code-block:: python

    import pkg_resources
        for x in pkg_resources.iter_group_name(None, None):
            print x

Using the Template
===================

Now that the entry point is working, a new project can be created:

.. code-block:: bash

    $ paster create --template=art TestProject

Paster will ask lots of questions based on the variables set up in ``vars`` earlier. Pressing ``return`` will cause the default to be used. The final result is a nice project template ready for people to start coding with.

Implementing Pylons Templates
=============================

If the development context is subject to a frequent need to create lots of Pylons projects, each with a slightly different setup from the standard Pylons defaults then it is probably desirable to create a customised Pylons template to use when generating projects. This can be done in exactly the way described in this document.

First, set up a new Python package, perhaps called something like ``CustomPylons`` (obviously, don't use the Pylons name because Pylons itself is already using it). Then check out the Pylons source code and copy the `pylons/templates/default_project <http://pylonshq.com/project/pylonshq/browser/Pylons/trunk/pylons/templates/default_project>`_ directory into the new project as a starting point. The next stage is to add the custom ``vars`` and ``Template`` class and set up the entry points in the ``CustomPylons`` ``setup.py`` file. 

After those tasks have been completed, it is then possible to create customised templates (ultimately based on the Pylons one) by using the ``CustomPylons`` package.

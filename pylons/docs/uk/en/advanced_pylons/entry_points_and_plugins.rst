.. _entry_points_and_plugins:

===================================
Using Entry Points to Write Plugins
===================================

Introduction
============

An entry point is a Python object in a project's code that is identified by a string in the project's ``setup.py`` file. The entry point is referenced by a group and a name so that the object may be discoverabe. This means that another application can search for all the installed software that has an entry point with a particular group name, and then access the Python object associated with that name. 

This is extremely useful because it means it is possible to write plugins for an appropriately-designed application that can be loaded at run time. This document describes just such an application.

It is important to understand that entry points are a feature of the new Python eggs package format and are *not* a standard feature of Python. To learn about eggs, their benefits, how to install them and how to set them up, see:

* `Python Eggs <http://peak.telecommunity.com/DevCenter/PythonEggs>`_
* `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_
* `Setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_

If reading the above documentation is inconvenient, suffice it to say that eggs are created via a similar ``setup.py`` file to the one used by Python's own `distutils <http://docs.python.org/lib/module-distutils.html>`_ module --- except that eggs have some powerful extra features such as entry points and the ability to specify module dependencies and have them automatically installed by ``easy_install`` when the application itself is installed.

For those developers unfamiliar with ``distutils``: it is the standard mechanism by which Python packages should be distributed. To use it, add a ``setup.py`` file to the desired project, insert the required metadata and specify the important files. The ``setup.py`` file can be used to issue various commands which create distributions of the pacakge in various formats for users to install.

Creating Plugins
================

This document describes how to use entry points to create a plugin mechansim which allows new types of content to be added to a content management system but we are going to start by looking at the plugin. 

Say the standard way the CMS creates a plugin is with the ``make_plugin()`` function. In order for a plugin to be a plugin it must therefore have the function which takes the same arguments as the :func:`make_plugin` function and returns a plugin. We are going to add some image plugins to the CMS so we setup a project with the following directory structure:

.. code-block:: text

    + image_plugins
      + __init__.py
    + setup.py

The ``image_plugins/__init__.py`` file looks like this:

.. code-block:: python

    def make_jpeg_image_plugin():
        return "This would return the JPEG image plugin"

    def make_png_image_plugin():
        return "This would return the PNG image plugin"

We have now defined our plugins so we need to define our entry points. First lets write a basic ``setup.py`` for the project:

.. code-block:: python

    from setuptools import setup, find_packages

    setup(
        name='ImagePlugins',
        version="1.0",
        description="Image plugins for the imaginary CMS 1.0 project",
        author="James Gardner",
        packages=find_packages(),
        include_package_data=True,
    )

When using ``setuptools`` we can specify the ``find_packages()`` function and ``include_package_data=True`` rather than having to manually list all the modules and package data like we had to do in the old ``distutils`` ``setup.py``. 

Because the plugin is designed to work with the (imaginary) CMS 1.0 package, we need to specify that the plugin requires the CMS to be installed too and so we add this line to the ``setup()`` function:

.. code-block:: python

        install_requires=["CMS>=1.0"],
  
Now when the plugins are installed, CMS 1.0 or above will be installed automatically if it is not already present.

There are lots of other arguments such as ``author_email`` or ``url`` which you can add to the ``setup.py`` function too.

We are interested in adding the entry points. We need to decide on a group name for the entry points. It is traditional to use the name of the package using the entry point, separated by a ``.`` character and then use a name that describes what the entry point does. For our example ``cms.plugin`` might be an appropriate name for the entry point. Since the ``image_plugin`` module contains two plugins we will need two entries. Add the following to the ``setup.py`` function:


.. code-block:: python

        entry_points="""
            [cms.plugin]
            jpg_image=image_plugin:make_jpeg_image_plugin
            png_image=image_plugin:make_jpeg_image_plugin
        """,

Group names are specified in square brackets, plugin names are specified in the format ``name=module.import.path:object_within_the_module``. The object doesn't have to be a function and can have any valid Python name. The module import path doesn't have to be a top level component as it is in this example and the name of the entry point doesn't have to be the same as the name of the object it is pointing to.

The developer can add as many entries as desired in each group as long as the names are different and the same holds for adding groups. It is also possible to specify the entry points as a Python dictionary rather than a string if that approach is preferred.

There are two more things we need to do to complete the plugin. The first is to include an ``ez_setup`` module so that if the user installing the plugin doesn't have ``setuptools`` installed, it will be installed for them. We do this by adding the follwoing to the very top of the ``setup.py`` file before the import:


.. code-block:: python

    from ez_setup import use_setuptools
    use_setuptools()


We also need to download the ``ez_setup.py`` file into our project directory at the same level as ``setup.py``.

.. note::

	If you keep your project in SVN there is a `trick you can use with the `SVN:externals <http://peak.telecommunity.com/DevCenter/setuptools#managing-multiple-projects>`_ to keep the ``ez_setup.py`` file up to date.

Finally in order for the CMS to find the plugins we need to install them. We can do this with:

.. code-block:: bash

    $ python setup.py install

as usual or, since we might go on to develop the plugins further we can install them using a special development mode which sets up the paths to run the plugins from the source rather than installing them to Python's ``site-packages`` directory:

.. code-block:: bash

	$ python setup.py develop

Both commands will download and install ``setuptools`` if you don't already have it installed.


Using Plugins
=============

Now that the plugin is written we need to write the code in the CMS package to load it. Luckily this is even easier. 

There are actually lots of ways of discovering plugins. For example: by distribution name and version requirement (such as ``ImagePlugins>=1.0``) or by the entry point group and name (eg ``jpg_image``). For this example we are choosing the latter, here is a simple script for loading the plugins:

.. code-block:: python

    from pkg_resources import iter_entry_points
    for object in iter_entry_points(group='cms.plugin', name=None):
        print object()

    from pkg_resources import iter_entry_points
    available_methods = []
    for method_handler in iter_entry_points(group='authkit.method', name=None):
        available_methods.append(method_handler.load())

Executing this short script, will result in the following output:

.. code-block:: text

    This would return the JPEG image plugin
    This would return the PNG image plugin

The ``iter_entry_points()`` function has looped though all the objects in the ``cms.plugin`` group and returned the function they were associated with. The application then called the function that the enrty point was pointing to.

We hope that we have demonstrated the power of entry points for building extensible code and developers are encouraged to read the `pkg_resources <http://peak.telecommunity.com/DevCenter/PkgResources>`_ module documentation to learn about some more features of the eggs format. 


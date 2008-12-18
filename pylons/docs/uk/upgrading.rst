.. _upgrading:

=========
Upgrading
=========

Upgrading your project is slightly different depending on which versions you're upgrading from and to. It's recommended that upgrades be done in minor revision steps, as deprecation warnings are added between revisions to help in the upgrade process.

For example, if you're running 0.9.4, first upgrade to 0.9.5, then 0.9.6, then finally 0.9.7 when desired. The change to 0.9.7 can be done in two steps unlike the older upgrades which should follow the process documented here after the 0.9.7 upgrade.


Upgrading from 0.9.6 -> 0.9.7
=============================

Pylons 0.9.7 changes several implicit behaviors of 0.9.6, as well as toggling some new options of Routes, and using automatic HTML escaping in Mako. These changes can be done in waves, and do not need to be completed all at once for a 0.9.6 project to run under 0.9.7.

Minimal Steps to run a 0.9.6 project under 0.9.7
------------------------------------------------

Add the following lines to ``config/environment.py``:

.. code-block:: python
    
    # Add these imports to the top
    from beaker.middleware import CacheMiddleware, SessionMiddleware
    from routes.middleware import RoutesMiddleware
    
    # Add these below the 'CUSTOM MIDDLEWARE HERE' line, or if you removed
    # that, add them immediately after the PylonsApp initialization
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)

The Rails helpers from WebHelpers are no longer automatically imported in the webhelpers package. To use them 'lib/helpers.py' should be changed to import them:

.. code-block:: python

    from webhelpers.rails import *

Your Pylons 0.9.6 project should now run without issue in Pylons 0.9.7. Note that some deprecation warnings will likely be thrown reminding you to upgrade other parts.

Moving to use the new features of 0.9.7
---------------------------------------

To use the complete set of new features in 0.9.7, such as the automatic HTML escaping, new webhelpers, and new error middleware, follow the
`What's new in Pylons 0.9.7 overview <http://wiki.pylonshq.com/pages/viewpage.action?pageId=11174779>`_ to determine how to change the other files in your project to use the new features.

Moving from a pre-0.9.6 to 0.9.6
================================

Pylons projects should be updated using the paster command create. In addition
to creating new projects, paster create when run over an existing project will
provide several ways to update the project template to the latest version. 

Using this tool properly can make upgrading a fairly minor task. For the 
purpose of this document, the project being upgraded will be called 'demoapp'
and all commands will use that name.

Running ``paster create`` to upgrade 
------------------------------------ 

First, navigate to the directory *above* the project's main directory. 
The main directory is the one that contains the ``setup.py``, ``setup.cfg``, and 
``development.ini`` files. 

.. code-block:: bash 

    /home/joe/demoapp $ cd .. 
    /home/joe $ 


Then run paster create on the project directory: 

.. code-block:: bash 

    /home/joe $ paster create demoapp -t pylons 


paster will issue prompts to allow the handling conflicts and updates to the existing 
project files. The options available are (hit the key in the parens to perform the 
operation): 

.. code-block:: text 

    (d)iff them, and show the changes between the project files and the ones 
    that have changed in Pylons
 
    (b)ackup the file and copy the new version into its place. The backup file that
    is created will have a ``.bak`` extension. 

    (y)es to overwrite the existing file with the new one. This approach is generally 
    not recommended as it does not allow the developer to view the content of the file
    that will be replaced and it offers no opportunity for later recovery of the content.
    The option can be made less intrepid by first viewing the diff to ascertain if any
    changes will be lost in the overwriting. 

    (n)o to overwrite, retain the existing file. Safe if nothing has changed. 

It's recommended when upgrading your project that you always look at the diff 
first to see what has changed. Then either overwrite your existing one if you are 
not going to lose changes you want, or backup yours and write the new one in. 
You can then manually compare and add your changes back in. 

.. _upgrading:

=========
Upgrading
=========

Upgrading your Pylons Project 
============================= 

Pylons projects should be updated using the paster command create. In addition 
to creating new projects, ``paster create`` when run within an existing project, 
provides several ways to update the project template to the latest version. 

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

.. _python23_installation:

====================================
Python 2.3 Installation Instructions
====================================

Advice of **end of support for Python 2.3**
-------------------------------------------

.. warning:: **END OF SUPPORT FOR PYTHON 2.3** This is the **LAST** version to support Python 2.3 **BEGIN UPGRADING OR DIE**

Preparation
-----------

First, please note that Python 2.3 users on Windows will need to install `subprocess.exe`__ before beginning the installation (whereas Python 2.4 users on Windows do not). All windows users also should read the section :ref:`windows_notes` after installation. Users of Ubuntu/debian will also likely need to install the python-dev package.

System-wide Install
-------------------

To install Pylons so it can be used by everyone (you'll need root access).

If you already have easy install:

.. code-block:: bash

    $ easy_install Pylons==0.9.7

.. note::
    On rare occasions, the python.org Cheeseshop goes down. It is still 
    possible to install Pylons and its dependencies however by specifying our
    local package directory for installation with:
    
    .. code-block:: bash
    
        $ easy_install -f http://pylonshq.com/download/ Pylons==0.9.7
    
    Which will use the packages necessary for the latest release. If you're 
    using an older version of Pylons, you can get the packages that went with
    it by specifying the version desired:
    
    .. code-block:: bash
    
        $ easy_install -f http://pylonshq.com/download/0.9.7/ Pylons==0.9.7

Otherwise: 

#. Download the easy install setup file from http://peak.telecommunity.com/dist/ez_setup.py
#. Run:

.. code-block:: bash

    $ python ez_setup.py Pylons==0.9.7


.. __: http://www.pylonshq.com/download/subprocess-0.1-20041012.win32-py2.3.exe

.. warning:: **END OF SUPPORT FOR PYTHON 2.3** This is the **LAST** version to support Python 2.3 **BEGIN UPGRADING OR DIE**

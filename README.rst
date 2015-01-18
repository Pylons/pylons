Pylons
++++++

.. image:: https://secure.travis-ci.org/Pylons/pylons.png?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/Pylons/pylons

Pylons is a rapid web application development framework.

`Read the complete Pylons web framework documentation
<http://docs.pylonsproject.org/projects/pylons-webframework/>`_

Install
=======

`Read the online Installation instructions
<http://docs.pylonsproject.org/projects/pylons-webframework/en/latest/gettingstarted.html#installing>`_.

If you want to install from source you can run the following command:

.. code-block :: bash

    $ python setup.py install

This will display a message and download setuptools if the module is not
already installed. It will then install Pylons and all its dependencies. You
may need root privileges to install setuptools.

Testing
=======

To test the source distribution run the following command:

.. code-block :: bash

    $ python setup.py test

This will install additional dependencies needed for the tests. As above, you
may need root privileges.

Documentation
=============

Generating documentation requires Sphinx:

.. code-block :: bash

    $ easy_install Sphinx

Then to build the documentation use the commands:

.. code-block :: bash

    $ cd pylons/docs/<lang>
    $ make html

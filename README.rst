Pylons
++++++

Pylons is a rapid web application development framework.

Full documentation is available online at http://pylonshq.com/docs/en/1.0/

Install
=======

Installation instructions are at http://pylonshq.com/docs/en/1.0/gettingstarted/

If you want to install from source you can run the following command:

.. code-block :: bash

    $ python setup.py install

This will display a message and download setuptools if the module is not
already installed. It will then install Pylons and all its dependencies. You
may need root privileges to install setuptools.

Testing
=======

To test the source distribution run the following command:

you will need to install Pylons as well some
additional tools.

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

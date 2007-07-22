Pylons
++++++

Pylons is a rapid web application development framework.

Full documentation is available online at http://pylonshq.com/docs/

Install
=======

Installation instructions are at http://pylonshq.com/install/

If you want to install from source you can run the following command:

.. code-block :: Bash

    python setup.py install

This will display a message and download setuptools if the module is not
already installed. It will then install Pylons and all its dependencies. You
may need root priveledges to install setuptools.

Testing
=======

To test the source distribution you will need to install Pylons as well some
additional tools.

.. code-block :: Bash

    easy_install TurboKid TurboCheetah "Kid==0.9.4" "Cheetah=2.0rc8"

Kid 0.9.6 does not currently pass the tests. Cheetah 2.0rc8 requires
compilation and is not available directly from the Cheeseshop. You can compile
and install it on Debian with these commands:

.. code-block :: Bash

    sudo apt-get install python-dev build-essential
    easy_install http://downloads.sourceforge.net/cheetahtemplate/Cheetah-2.0rc8.tar.gz?modtime=1176325572&big_mirror=0

Once the required packages are installed you can run the tests with the 
following command in the root of the source tree:

.. code-block :: Bash
    
    nosetests

Module Documentation
====================

Generating module documentation also requires specific tools. You will need to install subversion the issue the following commands:

.. code-block :: Bash

    easy_install "pudge==dev" Pygments "Buildutils==dev" TurboKid Kid

Then to build the documentation use this command:

.. code-block :: Bash

    python setup.py pudge -m pylons
    

.. _windows_notes:

=============
Windows Notes
=============

Python scripts installed as part of the Pylons install process will be put in the ``Scripts`` directory of your Python installation, typically in ``C:\Python24\Scripts``. By default on Windows, this directory is not in your ``PATH``; this can cause the following error message when running a command such as ``paster`` from the command prompt:

.. code-block:: text

	C:\Documents and Settings\James>paster
	'paster' is not recognized as an internal or external command,
	operable program or batch file.

To run the scripts installed with Pylons either the full path must be specified:

.. code-block:: text

	C:\Documents and Settings\James>C:\Python24\Scripts\paster
	Usage: C:\Python24\Scripts\paster-script.py COMMAND
	usage: paster-script.py [paster_options] COMMAND [command_options]

	options:
	  --version         show program's version number and exit
	  --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
			    specs; will also require() the Egg)
	  -h, --help        Show this help message
	
	... etc ...
	
or (the preferable solution) the ``Scripts`` directory must be added to the ``PATH`` as described below.

For Win2K or WinXP
------------------

#. From the desktop or Start Menu, right click My Computer and click Properties.
#. In the System Properties window, click on the Advanced tab.
#. In the Advanced section, click the Environment Variables button. 
#. Finally, in the Environment Variables window, highlight the path variable in the Systems Variable section and click edit. Add or modify the path lines with the paths you wish the computer to access. Each different directory is separated with a semicolon as shown below:

.. code-block:: text

	C:\Program Files;C:\WINDOWS;C:\WINDOWS\System32
      
#. Add the path to your scripts directory:

.. code-block:: text

	C:\Program Files;C:\WINDOWS;C:\WINDOWS\System32;C:\Python24\Scripts
	
See `Finally`_ below.
	
For Windows 95, 98 and ME
-------------------------

Edit ``autoexec.bat``, and add the following line to the end of the file:

.. code-block:: bash

	set PATH=%PATH%;C:\Python24\Scripts

See `Finally`_ below.

Finally
-------

Restarting your computer may be required to enable the change to the ``PATH``. Then commands may be entered from any location:

.. code-block:: text

	C:\Documents and Settings\James>paster
	Usage: C:\Python24\Scripts\paster-script.py COMMAND
	usage: paster-script.py [paster_options] COMMAND [command_options]

	options:
	  --version         show program's version number and exit
	  --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
			    specs; will also require() the Egg)
	  -h, --help        Show this help message
	
	... etc ...

All documentation assumes the ``PATH`` is setup correctly as described above.

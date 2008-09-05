.. _paster_commands: - Adding commands to paster

=========================
Adding commands to Paster
=========================

Paster command
==============

The command line will be ``paster my-command arg1 arg2`` if the current directory is the application egg, or ``paster --plugin=MyPylonsApp my-command arg1 arg2`` otherwise.  In the latter case, ``MyPylonsApp`` must have been installed via ``easy_install`` or ``python setup.py develop``.  

Make a package directory for your commands:

.. code-block:: bash

	$ mkdir myapp/commands
	$ touch myapp/commands/__init__.py

Create a module ``myapp/commands/my_command.py`` like this:

.. code-block:: python

	from paste.script.command import Command
	
	class MyCommand(Command):
		# Parser configuration
		summary = "--NO SUMMARY--"
		usage = "--NO USAGE--"
		group_name = "myapp"
		parser = Command.standard_parser(verbose=False)
	
		def command(self):
			import pprint
			print "Hello, app script world!"
			print
			print "My options are:"
			print "    ", pprint.pformat(vars(self.options))
			print "My args are:"
			print "    ", pprint.pformat(self.args)
			print
			print "My parser help is:"
			print
			print self.parser.format_help()

.. note:: The class _must_ define ``.command``, ``.parser``, and ``.summary``

Modify the ``entry_points`` argument in :file:`setup.py` to contain:

.. code-block:: python

	[paste.paster_command]
	my-command = myapp.commands.my_command:MyCommand


Run ``python setup.py develop`` or ``easy_install .`` to update the entry points in the egg in sys.path.

Now you should be able to run:

.. code-block:: bash

	$ paster --plugin=MyApp my-command arg1 arg2
	Hello, MyApp script world!

	My options are:
		 {'interactive': False, 'overwrite': False, 'quiet': 0, 'verbose': 0}
	My args are:
		 ['arg1', 'arg2']
	
	My parser help is:
	
	Usage: /usr/local/bin/paster my-command [options] --NO USAGE--
	--NO SUMMARY--
	
	Options:
	  -h, --help  show this help message and exit
	
	$ paster --plugin=MyApp --help
	Usage: paster [paster_options] COMMAND [command_options]
	
	...
	myapp:
	  my-command      --NO SUMMARY--
	
	pylons:
	  controller      Create a Controller and accompanying functional test
	  restcontroller  Create a REST Controller and accompanying functional test
	  shell           Open an interactive shell with the Pylons app loaded

Required class attributes
==========================

In addition to the ``.command`` method, the class should define ``.parser`` and ``.summary``.

Command-line options
====================

:func:`Command.standard_parser` returns a Python :obj:`OptionParser`.  Calling ``parser.add_option`` enables the developer to add as many options as desired.  Inside the ``.command`` method, the user's options are available under ``self.options``, and any additional arguments are in ``self.args``.  

There are several other class attributes that affect the parser; see them defined in ``paste.script.command:Command``.  The most useful attributes are ``.usage``, ``.description``, ``.min_args``, and ``.max_args``.   ``.usage`` is the part of the usage string _after_ the command name.  The ``.standard_parser()`` method has several optional arguments to add standardized options; some of these got added to my parser although I don't see how.

See the ``paster shell`` command, ``pylons.commands:ShellCommand``, for an example of using command-line options and loading the ``.ini file`` and model.  

Also see "paster setup-app" where it is defined in ``paste.script.appinstall.SetupCommand``.  This is evident from the entry point in PasteScript  (:file:`PasteScript-VERSION.egg/EGG_INFO/entry_points.txt`).  It is a complex example of reading a config file and delegating to another entry point. 

The code for calling ``myapp.websetup:setup_config`` is in ``paste.script.appinstall``.  

The ``Command`` class also has several convenience methods to handle console prompts, enable logging, verify directories exist and that files have expected content, insert text into a file, run a shell command, add files to Subversion, parse "var=value" arguments, add variables to an .ini file.

Using paster to access a Pylons app
===================================

Paster provides ``request`` and ``post`` commands for running requests on an application. These commands will be run in the full configuration context of a normal application.  Useful for cron jobs, the error handler will also be in place and you can get email reports of failed requests.

Because arguments all just go in ``QUERY_STRING``, ``request.GET`` and ``request.PARAMS`` won't look like you expect.  But you can parse them with
something like:

.. code-block:: python

  parser = optparse.OptionParser()
  parser.add_option(etc)

  args = [item[0] for item in
          cgi.parse_qsl(request.environ['QUERY_STRING'])]
  
  options, args = parser.parse_args(args)

paster request / post
---------------------

Usage: paster request / post [options] CONFIG_FILE URL [OPTIONS/ARGUMENTS]

Run a request for the described application

This command makes an artifical request to a web application that uses a
``paste.deploy`` configuration file for the server and application.  Use 'paster
request config.ini /url' to request ``/url``.

Use 'paster post config.ini /url < data' to do a POST with the given request body.

If the URL is relative (i.e. doesn't begin with /) it is interpreted as relative to /.command/.  

The variable ``environ['paste.command_request']`` will be set to True in the request, so your application can distinguish these calls from normal requests.  

Note that you can pass options besides the options listed here; any unknown options will be passed to the application in ``environ['QUERY_STRING']``.

.. code-block:: none

	Options:
	  -h, --help            show this help message and exit
	  -v, --verbose         
	  -q, --quiet           
	  -n NAME, --app-name=NAME
                                Load the named application (default main)
	  --config-var=NAME:VALUE
                                Variable to make available in the config for %()s
                                substitution (you can use this option multiple times)
	  --header=NAME:VALUE   Header to add to request (you can use this option
                                multiple times)
	  --display-headers     Display headers before the response body

Future development
------------------

A Pylons controller that handled some of this would probably be quite
useful.  Probably even nicer with additions to the current template, so
that ``/.command/`` all gets routed to a single controller that uses actions
for the various sub-commands, and can provide a useful response to
``/.command/?-h``, etc.

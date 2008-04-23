.. _configuration:

=============
Configuration
=============

XXX: Write overview of configuration choices, difference between run-time/deplyment configuration, and application configuration (whats in the config/ dir)


.. _run-config:

Runtime Configuration
=====================

XXX: Explain run-time config, the ini format used by development.ini and the
other ini files and how that affects the run-time configuration


.. _environment-config:

Environment
===========

The :file:`config/environment.py` module, sets up the basic Pylons environment
variables needed to run the application. Objects that should be setup once
for the entire application should either be setup here, or in the
:file:`lib/app_globals` :meth:`__init__.py` method.

It also calls the :ref:`url-config` function to setup how the URL's will
be matched up to your :ref:`controllers`, creates your :term:`app-globals`
object, configures which module will be referred to as :term:`h`, and is
where the template engine is setup.

If you're using SQLAlchemy, its recommended that you setup the SQLAlchemy
engine in this module. The default SQLAlchemy setup that Pylons comes with
creates the engine here which is then used in :file:`model/__init__.py`.


.. _url-config:

URL Configuration
=================

XXX: Explanation of how the default route can map to any controller, how to add routes, link to Routes manual


.. _middleware-config:

Middleware
==========

XXX: How to change the middleware, the purpose of full_stack, changing when
middleware is used in the stack


.. _setup-config:

Application Setup
=================

XXX: Explain how to setup app dependencies in the setup.py file to ensure
the appropriate libraries are required, explain what setup.py needs, etc.

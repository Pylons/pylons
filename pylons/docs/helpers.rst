.. _helpers:

=======
Helpers
=======

Helpers are functions intended for usage in templates, to assist with common
HTML and text manipulation, higher level constructs like a HTML
tag builder (that safely escapes variables), and advanced functionality
like Pagination of data sets.

The majority of the helpers available in Pylons are provided by the
:mod:`webhelpers` package. Some of these helpers are also used in controllers
to prepare data for use in the template by other helpers, such as the
:func:`~webhelpers.rails.secure_form_tag` function which has a corresponding 
:func:`~pylons.decorators.secure.authenticate_form`.

To make individual helpers available for use in templates under :term:`h`, the
appropriate functions need to be imported in :file:`lib/helpers.py`. All the
functions available in this file are then available under :term:`h` just like
any other module reference.

By customizing the :file:`lib/helpers.py` module you can quickly add custom
functions and classes for use in your templates.


.. _pagination:

Pagination
==========

XXX: Document using the webhelpers.paginate.Page class here, with examples of
setting it up in the controller, and the using the pager in the template


.. _secure-forms:

Secure Forms
============

XXX: Document using the secure_form_tag and authenticate_form function in the controller to prevent CSRF exploits.

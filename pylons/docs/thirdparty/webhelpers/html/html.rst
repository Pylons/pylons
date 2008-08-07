:mod:`~webhelpers.html` -- HTML handling
========================================
.. _webhelpers_html:

=============
HTML handling
=============

:mod:`webhelpers.html.builder`
-------------------------------

.. currentmodule:: webhelpers.html.builder

.. autoclass:: UnfinishedTag
    :members:
.. autoclass:: UnfinishedComment
    :members:
.. autoclass:: UnfinishedLiteral
    :members:
.. autoclass:: HTMLBuilder
    :members:
.. autofunction:: make_tag
.. autofunction:: literal
.. autofunction:: lit_sub
.. autofunction:: escape
.. autoclass:: _EscapedItem
    :members:

:mod:`webhelpers.html.converters`
----------------------------------

.. currentmodule:: webhelpers.html.converters

.. autofunction:: markdown
.. autofunction:: textilize

:mod:`webhelpers.html.secure_form`
-----------------------------------

.. currentmodule:: webhelpers.html.secure_form

.. autofunction:: authentication_token
.. autofunction:: auth_token_hidden_field
.. autofunction:: secure_form

:mod:`webhelpers.html.tags`
----------------------------

.. currentmodule:: webhelpers.html.tags

.. autofunction:: form
.. autofunction:: end_form
.. autofunction:: text
.. autofunction:: hidden
.. autofunction:: file
.. autofunction:: password
.. autofunction:: textarea
.. autofunction:: checkbox
.. autofunction:: _make_safe_id_component
.. autofunction:: radio
.. autofunction:: submit
.. autofunction:: select
.. autoclass:: ModelTags
    :members:
.. autofunction:: link_to
.. autofunction:: link_to_if
.. autofunction:: link_to_unless
.. autofunction:: th_sortable
.. autofunction:: image
.. autofunction:: javascript_link
.. autofunction:: stylesheet_link
.. autofunction:: auto_discovery_link

:mod:`webhelpers.html.tools`
-----------------------------

.. currentmodule:: webhelpers.html.tools

.. autofunction:: button_to
.. autofunction:: mail_to
.. autofunction:: highlight
.. autofunction:: auto_link
.. autofunction:: strip_links


:mod:`webhelpers` -- Web helpers
================================
.. _webhelpers:

==========
WebHelpers
==========

.. automodule:: webhelpers

:mod:`webhelpers.constants`
----------------------------
.. currentmodule:: webhelpers.constants

.. automodule:: webhelpers.constants
.. autofunction:: uk_counties
.. autofunction:: country_codes
.. autofunction:: timezones
.. autofunction:: timezones_for_country


:mod:`webhelpers.containers`
----------------------------
.. currentmodule:: webhelpers.containers

.. automodule:: webhelpers.containers
.. autoclass:: Flash
    :members:

:mod:`webhelpers.date`
----------------------
.. currentmodule:: webhelpers.date

.. automodule:: webhelpers.date
.. autofunction:: distance_of_time_in_words


:mod:`webhelpers.feedgenerator`
--------------------------------
.. currentmodule:: webhelpers.feedgenerator

.. automodule:: webhelpers.feedgenerator
.. autoclass:: SyndicationFeed
    :members:

.. autoclass:: Enclosure
    :members:

.. autoclass:: RssFeed
    :members:

.. autoclass:: RssUserland091Feed
    :members:

.. autoclass:: Rss201rev2Feed
    :members:

.. autoclass:: Atom1Feed
    :members:

.. autofunction:: rfc2822_date
.. autofunction:: rfc3339_date
.. autofunction:: get_tag_uri

:mod:`webhelpers.html.builder`
------------------------------
.. currentmodule:: webhelpers.html.builder

.. automodule:: webhelpers.html.builder
.. autoclass::  HTMLBuilder

:mod:`webhelpers.html.converters`
---------------------------------
.. currentmodule:: webhelpers.html.converters

.. automodule:: webhelpers.html.converters

.. autofunction:: markdown
.. autofunction:: textilize

:mod:`webhelpers.html.tags`
----------------------------
.. currentmodule:: webhelpers.html.tags

.. automodule:: webhelpers.html.tags
.. autofunction:: form
.. autofunction:: end_form
.. autofunction:: text
.. autofunction:: textarea
.. autofunction:: hidden
.. autofunction:: file
.. autofunction:: password
.. autofunction:: text
.. autofunction:: checkbox
.. autofunction:: radio
.. autofunction:: submit
.. autofunction:: select
.. autofunction:: ModelTags
.. autofunction:: link_to
.. autofunction:: link_to_if
.. autofunction:: link_to_unless
.. autofunction:: image
.. autofunction:: auto_discovery_link
.. autofunction:: javascript_link
.. autofunction:: javascript_path
.. autofunction:: stylesheet_link
.. autofunction:: convert_boolean_attrs

:mod:`webhelpers.html.tools`
----------------------------
.. currentmodule:: webhelpers.html.tools

.. automodule:: webhelpers.html.tools

.. autofunction:: button_to
.. autofunction:: mail_to
.. autofunction:: highlight
.. autofunction:: strip_links
.. autofunction:: auto_link

:mod:`webhelpers.mail`
----------------------
.. currentmodule:: webhelpers.mail

.. automodule:: webhelpers.mail

.. autofunction:: plain
.. autofunction:: part
.. autofunction:: multi
.. autofunction:: send

:mod:`webhelpers.markdown`
--------------------------
.. currentmodule:: webhelpers.markdown

.. automodule:: webhelpers.markdown
.. autofunction:: markdown

:mod:`webhelpers.paginate`
--------------------------
.. automodule:: webhelpers.paginate

.. autoclass:: Page
    :members:

.. automethod:: Page.pager

:mod:`webhelpers.text`
----------------------
.. currentmodule:: webhelpers.text

.. automodule:: webhelpers.text
.. autofunction:: truncate
.. autofunction:: excerpt

:mod:`webhelpers.textile`
-------------------------
.. currentmodule:: webhelpers.textile

.. automodule:: webhelpers.textile

:mod:`webhelpers.util`
----------------------
.. currentmodule:: webhelpers.util

.. automodule:: webhelpers.util
.. autoclass:: SimplerXMLGenerator
.. autoclass:: UnicodeMultiDict

.. autofunction:: iri_to_uri
.. autofunction:: html_escape

:mod:`webhelpers.rails.asset_tag`
---------------------------------
.. currentmodule:: webhelpers.rails.asset_tag

.. automodule:: webhelpers.rails.asset_tag
.. autofunction:: auto_discovery_link_tag
.. autofunction:: image_tag
.. autofunction:: javascript_include_tag
.. autofunction:: stylesheet_link_tag
.. autofunction:: compute_public_path
.. autofunction:: get_script_name

:mod:`webhelpers.rails.date`
----------------------------
.. currentmodule:: webhelpers.rails.date

.. automodule:: webhelpers.rails.date
.. autofunction:: time_ago_in_words
.. autofunction:: distance_of_time_in_words

:mod:`webhelpers.rails.form_options`
-------------------------------------
.. currentmodule:: webhelpers.rails.form_options

.. automodule:: webhelpers.rails.form_options

.. autofunction:: options_for_select
.. autofunction:: options_for_select_from_objects
.. autofunction:: options_for_select_from_dicts

:mod:`webhelpers.rails.form_tag`
--------------------------------
.. currentmodule:: webhelpers.rails.form_tag

.. automodule:: webhelpers.rails.form_tag

.. autofunction:: form
.. autofunction:: end_form
.. autofunction:: select
.. autofunction:: text_field
.. autofunction:: hidden_field
.. autofunction:: file_field
.. autofunction:: password_field
.. autofunction:: text_area
.. autofunction:: check_box
.. autofunction:: radio_button
.. autofunction:: submit

:mod:`webhelpers.rails.javascript`
----------------------------------
.. currentmodule:: webhelpers.rails.javascript

.. automodule:: webhelpers.rails.javascript
.. autofunction:: link_to_function
.. autofunction:: button_to_function
.. autofunction:: escape_javascript
.. autofunction:: javascript_tag
.. autofunction:: javascript_cdata_section
.. autofunction:: options_for_javascript
.. autofunction:: array_or_string_for_javascript

:mod:`webhelpers.rails.number`
------------------------------
.. currentmodule:: webhelpers.rails.number

.. automodule:: webhelpers.rails.number
.. autofunction:: number_to_phone
.. autofunction:: number_to_currency
.. autofunction:: number_to_percentage
.. autofunction:: number_to_human_size
.. autofunction:: human_size
.. autofunction:: number_with_delimiter
.. autofunction:: number_with_precision

:mod:`webhelpers.rails.prototype`
---------------------------------
.. currentmodule:: webhelpers.rails.prototype

.. automodule:: webhelpers.rails.prototype

.. autofunction:: link_to_remote
.. autofunction:: periodically_call_remote
.. autofunction:: form_remote_tag
.. autofunction:: submit_to_remote
.. autofunction:: update_element_function
.. autofunction:: evaluate_remote_response
.. autofunction:: remote_function
.. autofunction:: observe_field
.. autofunction:: observe_form
.. autofunction:: options_for_ajax
.. autofunction:: build_observer
.. autofunction:: build_callbacks

:mod:`webhelpers.rails.scriptaculous`
-------------------------------------
.. currentmodule:: webhelpers.rails.scriptaculous

.. automodule:: webhelpers.rails.scriptaculous
.. autofunction:: _elements_to_js
.. autofunction:: visual_effect
.. autofunction:: parallel_effects
.. autofunction:: sortable_element
.. autofunction:: sortable_element_js
.. autofunction:: draggable_element
.. autofunction:: draggable_element_js
.. autofunction:: drop_receiving_element
.. autofunction:: drop_receiving_element_js

:mod:`webhelpers.rails.secure_form_tag`
---------------------------------------
.. currentmodule:: webhelpers.rails.secure_form_tag

.. automodule:: webhelpers.rails.secure_form_tag
.. autofunction:: get_session
.. autofunction:: authentication_token
.. autofunction:: secure_form
.. autofunction:: secure_form_remote_tag
.. autofunction:: secure_button_to

:mod:`webhelpers.rails.tags`
----------------------------
.. currentmodule:: webhelpers.rails.tags

.. automodule:: webhelpers.rails.tags
.. autofunction:: camelize
.. autofunction:: strip_unders
.. autofunction:: tag
.. autofunction:: content_tag
.. autofunction:: cdata_section
.. autofunction:: escape_once
.. autofunction:: fix_double_escape
.. autofunction:: tag_options
.. autofunction:: convert_booleans
.. autofunction:: boolean_attribute

:mod:`webhelpers.rails.text`
----------------------------
.. currentmodule:: webhelpers.rails.text

.. automodule:: webhelpers.rails.text
.. autofunction:: iterdict
.. autofunction:: cycle
.. autofunction:: reset_cycle
.. autofunction:: counter
.. autofunction:: reset_counter
.. autofunction:: truncate
.. autofunction:: highlight
.. autofunction:: excerpt
.. autofunction:: word_wrap
.. autofunction:: simple_format
.. autofunction:: auto_link
.. autofunction:: auto_link_urls
.. autofunction:: auto_link_email_addresses
.. autofunction:: strip_links
.. autofunction:: textilize
.. autofunction:: markdown

:mod:`webhelpers.rails.urls`
----------------------------
.. currentmodule:: webhelpers.rails.urls

.. automodule:: webhelpers.rails.urls
.. autofunction:: get_url
.. autofunction:: url
.. autofunction:: link_to
.. autofunction:: button_to
.. autofunction:: _button_to
.. autofunction:: link_to_unless_current
.. autofunction:: link_to_unless
.. autofunction:: link_to_if
.. autofunction:: current_page
.. autofunction:: current_url
.. autofunction:: convert_options_to_javascript
.. autofunction:: convert_boolean_attributes
.. autofunction:: confirm_javascript_function
.. autofunction:: popup_javascript_function
.. autofunction:: method_javascript_function
.. autofunction:: mail_to
.. autofunction:: js_obfuscate



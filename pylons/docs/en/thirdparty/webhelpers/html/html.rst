:mod:`webhelpers.html` -- HTML handling
========================================

:mod:`webhelpers.html.builder`
-------------------------------

HTML/XHTML tag builder
----------------------

HTML Builder provides an ``HTML`` object that creates (X)HTML tags in a
Pythonic way,  a ``literal`` class used to mark strings containing intentional
HTML markup, and a smart ``escape()`` function that preserves literals but
escapes other strings that may accidentally contain markup characters ("<",
">", "&") or malicious Javascript tags.  Escaped strings are returned as
literals to prevent them from being double-escaped later.

``literal`` is a subclass of ``unicode``, so it works with all string methods
and expressions.  The only thing special about it is the ``.__html__`` method,
which returns the string itself.  ``escape()`` follows a simple protocol: if
the object has an ``.__html__`` method, it calls that rather than ``.__str__``
to get the HTML representation.  Third-party libraries that do not want to
import ``literal`` (and this create a dependency on WebHelpers) can put an
``.__html__`` method in their own classes returning the desired HTML
representation.

When used in a mixed expression containing both literals and ordinary strings,
``literal`` tries hard to escape the strings and return a literal.  However,
this depends on which value has "control" of the expression.  ``literal`` seems
to be able to take control with all combinations of the ``+`` operator, but
with ``%`` and ``join`` it must be on the left side of the expression.  So
these all work::

    "A" + literal("B")
    literal(", ").join(["A", literal("B")])
    literal("%s %s") % (16, literal("kg"))

But these return an ordinary string which is prone to double-escaping later::

    "\\n".join([literal('<span class="foo">Foo!</span>'), literal('Bar!')])
    "%s %s" % (literal("16"), literal("&lt;em&gt;kg&lt;/em&gt;"))

Third-party libraries that don't want to import ``literal`` and thus avoid a
dependency on WebHelpers can add an ``.__html__`` method to any class, which
can return the same as ``.__str__`` or something else.  ``escape()`` trusts the
HTML method and does not escape the return value.  So only strings that lack
an ``.__html__`` method will be escaped.

The ``HTML`` object has the following methods for tag building:

``HTML(*strings)``
    Escape the string args, concatenate them, and return a literal.  This is
    the same as ``escape(s)`` but accepts multiple strings.  Multiple args are
    useful when mixing child tags with text, such as::

        html = HTML("The king is a >>", HTML.strong("fink"), "<<!")

``HTML.literal(*strings)``
    Same as ``literal`` but concatenates multiple arguments.

``HTML.comment(*strings)``
    Escape and concatenate the strings, and wrap the result in an HTML 
    comment.

``HTML.tag(tag, *content, **attrs)``
    Create an HTML tag ``tag`` with the keyword args converted to attributes.
    The other positional args become the content for the tag, and are escaped
    and concatenated.  If an attribute name conflicts with a Python keyword
    (notably "class"), append an underscore.  If an attribute value is
    ``None``, the attribute is not inserted.  Two special keyword args are
    recognized:
    
    ``c``
        Specifies the content.  This cannot be combined with content in
        positional args.  The purpose of this argument is to position the
        content at the end of the argument list to match the native HTML
        syntax more closely.  Its use is entirely optional.  The value can
        be a string, a tuple, or a tag.

    ``_close``
        If present and false, do not close the tag.  Otherwise the tag will be
        closed with a closing tag or an XHTML-style trailing slash as described
        below.

    Example:

    .. code-block:: python

        >>> HTML.tag("a", href="http://www.yahoo.com", name=None, 
        ... c="Click Here")
        literal(u'<a href="http://www.yahoo.com">Click Here</a>')


``HTML.__getattr__``
    Same as ``HTML.tag`` but using attribute access.  Example:

    .. code-block:: python

        >>> HTML.a("Foo", href="http://example.com/", class_="important")
        literal(u'<a class="important" href="http://example.com/">Foo</a>')

The protocol is simple: if an object has an ``.__html__`` method, ``escape()``
calls it rather than ``.__str__()`` to obtain a string representation.

About XHTML and HTML
--------------------

This builder always produces tags that are valid as *both* HTML and
XHTML.  "Empty" tags (like ``<br>``, ``<input>`` etc) are written like ``<br />``,
with a space and a trailing ``/``.

*Only* empty tags get this treatment.  The library will never, for example,
product ``<script src="..." />``, which is invalid HTML.

The `W3C HTML validator <http://validator.w3.org/>`_ validates these
constructs as valid HTML Strict.  It does produce warnings, but those
warnings warn about the ambiguity if this same XML-style self-closing
tags are used for HTML elements that can take content (``<script>``,
``<textarea>``, etc).  This library never produces markup like that.

Rather than add options to generate different kinds of behavior, we
felt it was better to create markup that could be used in different
contexts without any real problems and without the overhead of passing
options around or maintaining different contexts, where you'd have to
keep track of whether markup is being rendered in an HTML or XHTML
context.

If you _really_ want tags without training slashes (e.g., ``<br>`)`, you can
"abuse" ``_close=False`` to produce them.


.. currentmodule:: webhelpers.html.builder

.. autoclass:: UnfinishedTag
    :members:
.. autoclass:: UnfinishedComment
    :members:
.. autoclass:: UnfinishedLiteral
    :members:
.. autoclass:: HTMLBuilder
.. autofunction:: make_tag
.. function:: literal

    Represents an HTML literal.
    
    This subclass of unicode has a ``.__html__()`` method that is 
    detected by the ``escape()`` function.
    
    Also, if you add another string to this string, the other string 
    will be quoted and you will get back another literal object.  Also
    ``literal(...) % obj`` will quote any value(s) from ``obj``.  If
    you do something like ``literal(...) + literal(...)``, neither
    string will be changed because ``escape(literal(...))`` doesn't
    change the original literal.

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


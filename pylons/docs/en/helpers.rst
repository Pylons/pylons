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

Helper functions are organized into modules by theme. All HTML generators are under the ``webhelpers_html`` package, except for a few third-party modules which are directly under ``webhelpers``. The webhelpers modules are separately documented, see :mod:`webhelpers`.

.. _pagination:

Pagination
==========

.. note::

    The `paginate` module is not compatible to the deprecated `pagination`
    module that was provided with former versions of the Webhelpers package.


Purpose of a paginator
----------------------

When you display large amounts of data like a result from an SQL query then
usually you cannot display all the results on a single page. It would simply be
too much. So you divide the data into smaller chunks. This is what a paginator
does. It shows one page of chunk of data at a time. Imagine you are providing a
company phonebook through the web and let the user search the entries. Assume
the search result contains 23 entries. You may decide to display no more than 10
entries per page. The first page contains entries 1-10, the second 11-20 and the
third 21-23. And you also show a navigational element like
``Page 1 of 3: [1] 2 3`` that allows the user to switch between the available
pages.


The ``Page`` class
------------------

The :mod:`webhelpers` package provides a *paginate* module that can be used
for this purpose. It can create pages from simple Python lists as well as
SQLAlchemy queries and SQLAlchemy select objects. The module provides a ``Page``
object that represents a single page of items from a larger result set. Such a
``Page`` mainly behaves like a list of items on that page. Let's take the above
example of 23 items spread across 3 pages:

.. code-block :: pycon
       
    # Create a list of items from 1 to 23
    >>> items = range(1,24)
    
    # Import the paginate module
    >>> import webhelpers.paginate
    
    # Create a Page object from the 'items' for the second page
    >>> page2 = webhelpers.paginate.Page(items, page=2, items_per_page=10)

    # The Page object can be printed (__repr__) to show details on the page
    >>> page2

        Page:
        Collection type:  <type 'list'>
        (Current) page:   2
        First item:       11
        Last item:        20
        First page:       1
        Last page:        3
        Previous page:    1
        Next page:        3
        Items per page:   10
        Number of items:  23
        Number of pages:  3

    # Show the items on this page
    >>> list(page2)
    
        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # Print the items in a for loop
    >>> for i in page2: print "This is entry", i

        This is entry 11
        This is entry 12
        This is entry 13
        This is entry 14
        This is entry 15
        This is entry 16
        This is entry 17
        This is entry 18
        This is entry 19
        This is entry 20

There are further parameters to invoking a ``Page`` object. Please see
:class:`webhelpers.paginate.Page`

.. note::

    Page numbers and item numbers start from 1. If you are accessing the
    items on the page by their index please note that the first item is
    ``item[1]`` instead of ``item[0]``.


Switching between pages using a `pager`
---------------------------------------

The user needs a way to get to another page. This is usually done with a list
of links like ``Page 3 of 41 - 1 2 [3] 4 5 .. 41``. Such a list can be
created by the Page's :meth:`~webhelpers.paginate.Page.pager` method.
Take the above example again:

.. code-block:: pycon

    >>> page2.pager()
    
        <a class="pager_link" href="/content?page=1">1</a>
        <span class="pager_curpage">2</span>
        <a class="pager_link" href="/content?page=3">3</a>

Without the HTML tags it looks like ``1 [2] 3``. The links point to a URL
where the respective page is found. And the current page (2) is highlighted.

The appearance of a pager can be customized. By default the format string
is ``~2~`` which means it shows adjacent pages from the current page with
a maximal radius of 2. In a larger set this would look like
``1 .. 34 35 [36] 37 38 .. 176``. The radius of 2 means that two pages before
and after the current page 36 are shown.

Several special variables can be used in the format string. See
:meth:`~webhelpers.paginate.Page.pager` for a complete list. Some examples
for a pager of 20 pages while being on page 10 currently:

.. code-block:: pycon

    >>> page.pager()
    
        1 .. 8 9 [10] 11 12 .. 20
        
    >>> page.pager('~4~')
    
        1 .. 6 7 8 9 [10] 11 12 13 14 .. 20
        
    >>> page.pager('Page $page of $page_count - ~3~')
    
        Page 10 of 20 - 1 .. 7 8 9 [10] 11 12 13 .. 20
        
    >>> page.pager('$link_previous $link_next ~2~')
    
        < > 1 .. 8 9 [10] 11 12 .. 20
        
    >>> page.pager('Items $first_item - $last_item / ~2~')
    
        Items 91 - 100 / 1 .. 8 9 [10] 11 12 .. 20


Paging over an SQLAlchemy query
-------------------------------

If the data to page over comes from a database via SQLAlchemy then the
``paginate`` module can access a ``query`` object directly. This is useful
when using ORM-mapped models. Example:

.. code-block:: pycon

    >>> employee_query = Session.query(Employee)
    >>> page2 = webhelpers.paginate.Page(
            employee_query,
            page=2,
            items_per_page=10)
    >>> for employee in page2: print employee.first_name

        John
        Jack
        Joseph
        Kay
        Lars
        Lynn
        Pamela
        Sandra
        Thomas
        Tim

The `paginate` module is smart enough to only query the database for the
objects that are needed on this page. E.g. if a page consists of the items
11-20 then SQLAlchemy will be asked to fetch exactly that 10 rows
through `LIMIT` and `OFFSET` in the actual SQL query. So you must not load
the complete result set into memory and pass that. Instead always pass
a `query` when creating a `Page`.


Paging over an SQLAlchemy select
--------------------------------

SQLAlchemy also allows to run arbitrary SELECTs on database tables.
This is useful for non-ORM queries. `paginate` can use such select
objects, too. Example:

.. code-block:: pycon

    >>> selection = sqlalchemy.select([Employee.c.first_name])
    >>> page2 = webhelpers.paginate.Page(
            selection,
            page=2,
            items_per_page=10,
            sqlalchemy_session=model.Session)
    >>> for first_name in page2: print first_name
    
        John
        Jack
        Joseph
        Kay
        Lars
        Lynn
        Pamela
        Sandra
        Thomas
        Tim

The only difference to using SQLAlchemy *query* objects is that you need to
pass an SQLAlchemy *session* via the ``sqlalchemy_session`` parameter.
A bare ``select`` does not have a database connection assigned. But the session
has.


Usage in a Pylons controller and template
-----------------------------------------

A simple example to begin with.

Controller:

.. code-block:: python

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5)
        return render('/employees/list.mako')

Template:

.. code-block:: mako

    ${c.employees.pager('Page $page: $link_previous $link_next ~4~')}
    <ul>
    % for employee in c.employees:
        <li>${employee.first_name} ${employee.last_name}</li>
    % endfor
    </ul>

The `pager()` creates links to the previous URL and just sets the
*page* parameter appropriately. That's why you need to pass the requested page
number (``request.params['page']``) when you create a `Page`.


Partial updates with AJAX
-------------------------

Updating a page partially is easy. All it takes is a little Javascript
that - instead of loading the complete page - updates just the part
of the page containing the paginated items. The ``pager()`` method accepts an
``onclick`` parameter for that purpose. This value is added as an ``onclick``
parameter to the A-HREF tags. So the ``href`` parameter points to a URL
that loads the complete page while the ``onclick`` parameter provides Javascript
that loads a partial page. An example (using the jQuery Javascript library for
simplification) may help explain that.

Controller:

.. code-block:: python

    def list(self):
        c.employees = webhelpers.paginate.Page(
            model.Session.query(model.Employee),
            page = int(request.params['page']),
            items_per_page = 5)
        if 'partial' in request.params:
            # Render the partial page
            return render('/employees/list-partial.mako')
        else:
            # Render the full page
            return render('/employees/list-full.mako')

Template ``list-full.mako``:

.. code-block:: mako

    <html>
        <head>
            ${webhelpers.html.tags.javascript_link('/public/jQuery.js')}
        </head>
        <body>
            <div id="page-area">
                <%include file="list-partial.mako"/>
            </div>
        </body>
    </html>

Template ``list-partial.mako``:

.. code-block:: mako

    ${c.employees.pager(
        'Page $page: $link_previous $link_next ~4~',
        onclick="$('#my-page-area').load('%s'); return false;")}
    <ul>
    % for employee in c.employees:
        <li>${employee.first_name} ${employee.last_name}</li>
    % endfor
    </ul>

To avoid code duplication in the template the full template includes the partial
template. If a partial page load is requested then just the
``list-partial.mako`` gets rendered. And if a full page load is requested then
the ``list-full.mako`` is rendered which in turn includes the
``list-partial.mako``.

The ``%s`` variable in the ``onclick`` string gets replaced with a URL pointing
to the respective page with a ``partial=1`` added (the name of the parameter can be customized through the ``partial_param`` parameter). Example:

* ``href`` parameter points to ``/employees/list?page=3``
* ``onclick`` parameter contains Javascript loading
  ``/employees/list?page=3&partial=1``

jQuery's syntax to load a URL into a certain DOM object (e.g. a DIV) is simply:

.. code-block:: javascript

    $('#some-id').load('/the/url')

The advantage of this technique is that it degrades gracefully. If the user does
not have Javascript enabled then a full page is loaded. And if Javascript works
then a partial load is done through the ``onclick`` action.


.. _secure-forms:

Secure Form Tag Helpers
=======================

For prevention of Cross-site request forgery (CSRF) attacks.

Generates form tags that include client-specific authorization tokens to be
verified by the destined web app.

Authorization tokens are stored in the client's session. The web app can then
verify the request's submitted authorization token with the value in the
client's session.

This ensures the request came from the originating page. See the wikipedia entry
for `Cross-site request forgery`__ for more information.

.. __: http://en.wikipedia.org/wiki/Cross-site_request_forgery

Pylons provides an ``authenticate_form`` decorator that does this verification
on the behalf of controllers.

These helpers depend on Pylons' ``session`` object.  Most of them can be easily 
ported to another framework by changing the API calls.

The helpers are implemented in such a way that it should be easy for developers
to create their own helpers if using helpers for AJAX calls.

:func:`authentication_token` returns the current authentication token, creating one
and storing it in the session if it doesn't already exist.

:func:`auth_token_hidden_field` creates a hidden field containing the authentication token.

:func:`secure_form` is :func:`form` plus :func:`auth_token_hidden_field`.


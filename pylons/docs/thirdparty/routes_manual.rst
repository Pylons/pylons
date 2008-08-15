.. _routes_manual: Routes Manual

=============
Routes Manual
=============

.. contents:: Table of Contents

------------
Introduction
------------

Routes tackles an interesting problem that comes up frequently in web
development, *how do you map a URL to your code?* While there are many
solutions to this problem, that range from using the URL paths as an object
publishing hierarchy, to regular expression matching; Routes goes a slightly
different way.

Using Routes, you specify parts of the URL path and how to match them to your
**Controllers** and **Actions**. The specific web framework you're using may
actually call them by slightly different names, but for the sake of consistency
we will use these names.

Routes lets you have multiple ways to get to the same Controller and Action, 
and uses an intelligent lookup mechanism to try and guarantee you the URL with
the **least cruft when generating the URL**.

URL Cruft
    Shorthand reference to what will occur if a Route can't handle all the 
    arguments we want to send it. Those arguments become HTTP query args 
    (/something *?query=arg&another=arg* ), which we try to avoid when
    generating a URL.
    
-----------------
Setting Up Routes
-----------------

To setup Routes, it is assumed that you are using a web framework that has the
Routes mechanism integrated for you. The web framework should have somewhere
setup for you to add a Route to your Mapper.

Route
    A Route is a mapping of a URL to a controller, action, and/or additional
    variables. Matching a Route will *always* result in a controller and
    action. Route objects are typically created and managed by the Mapper.

Mapper
    The Mapper is the main class used to hold, organize, and match Routes. 
    While you can create a Route object independently of the Mapper, its not
    nearly as useful. The Mapper is what you will use to add Routes and what
    the web framework uses to match incoming URLs.

We will also assume for this introduction that your Mapper instance is exposed
to you as ``m``, for example:

.. code-block:: python

    m = Mapper()
    m.connect(':controller/:action/:id')

The above example covers one of the most common routes that is typically
considered the *default route*. This very flexible route allows virtually all
of your controllers and actions to be called. Adding more routes is done in a
similar manner, by calling ``m.connect(...)`` and giving the Mapper instance a
set of arguments.

The following are all valid examples of adding routes:

.. code-block:: python

    m.connect('archives/:year/:month/:day', controller='archives', 
              action='view', year=2004,
              requirements=dict(year='\d{2,4}', month='\d{1,2}'))
    m.connect('feeds/:category/atom.xml', controller='feeds', action='atom')
    m.connect('history', 'archives/by_eon/:century', controller='archives', 
              action='aggregate', century=1800)
    m.connect('article', 'article/:section/:slug/:page.html', 
              controller='article', action='view')
    m.connect(':controller/:action/:id')
    m.connect('home', '', controller='blog', action='index')
    
In the following sections, we'll highlight the section of the Route we're
referring to in the first example.

Route Name
----------

*Optional*

    ``m.connect(`` 'history' ``, 'archives/by_eon/:century', controller='archives...``

A Route can have a name, this is also referred to as **Named Routes** and lets
you quickly reference the `Defaults`_ that the route was configured with. This
is the first non-keyword argument, and if not present the first non-keyword
argument is assumed to be the `route path`_.

Route Names are mainly used when generating routes, and have no other effect on
matching a URL.

Static Named Routes
^^^^^^^^^^^^^^^^^^^

With the release of 1.2, Routes now supports static named routes. These are
routes that do not involve actual URL generation, but instead allow you to
quickly alias common URLs. For example:

    ``m.connect('google_search',`` 'http://www.google.com/search', _static=True ``)``

Static Named Routes are ignored entirely when matching a URL.

Filter Functions
^^^^^^^^^^^^^^^^

Named routes can have functions associated with them that will operate on the
arguments used during generation. If you have a route that requires multiple
arguments to generate, like:

.. code-block:: python
    
    m.connect('archives/:year/:month/:day', controller='archives', 
              action='view', year=2004,
              requirements=dict(year='\d{2,4}', month='\d{1,2}'))

To generate a URL for this will require a month and day argument, and a year
argument if you don't want to use 2004. When using Routes with a database or
other objects that might have all this information, it's useful to let Routes
expand that information so you don't have to.

Consider the case where you have a ``story`` object which has a ``year``,
``month``, and ``day`` attribute. You could generate the URL with:

.. code-block:: python
    
    url_for(year=story.year, month=story.month, day=story.day)

This isn't terribly convenient, and can be brittle if for some reason you need
to change the ``story`` objects interface. Here's an example of setting up a
filter function:

.. code-block:: python
    
    def story_expand(kargs):
        # Only alter args if a story keyword arg is present
        if 'story' not in kargs:
            return kargs
        
        story = kargs.pop('story')
        kargs['year'] = story.year
        kargs['month'] = story.month
        kargs['day'] = story.day
        
        return kargs
    
    m.connect('archives', 'archives/:year/:month/:day', 
              controller='archives', action='view', year=2004,
              requirements=dict(year='\d{2,4}', month='\d{1,2}'),
              _filter=story_expand)
    
This filter function will be used when using the named route ``archives``. If a
``story`` keyword argument is present, it will use that and alter the keyword
arguments used to generate the actual route.

If you have a ``story`` object with those attributes, making the route would
now be done with the following arguments:

.. code-block:: python
    
    url_for('archives', story=my_story)

If the story interface changes, you can change how the arguments are pulled out
in a single location. This also makes it substantially easier to generate the
URL.

.. warning::

    Using the filter function *requires* the route to be a 
    `named route <named routes>`_. This is due to how the filter function can 
    affect the route that actually gets chosen. The only way to reliably ensure
    the proper filter function gets used is by naming the route, and using its
    route name with ``url_for``.

Route Path
----------

*Required*

    ``m.connect(``'feeds/:category/atom.xml'``, controller='feeds', action='atom')``
    
The Route Path determines the URL mapping for the Route. In the above example
a URL like ``/feeds/electronics/atom.xml`` will match this route.

A Route Path is separated into parts that you define, the naming used when
referencing the different types of route parts are:
 
_`Static Part`
    ``m.connect('`` feeds ``/:category/`` atom.xml ``', controller='feeds', action='atom')``

    A plain-text part of the URL, this doesn't result in any Route variables.

_`Dynamic Part`
    ``m.connect('feeds/`` :category ``/atom.xml', controller='feeds', action='atom')``
    
    A dynamic part matches text in that part of the URL, and assigns what it
    finds to the name after the ``:`` mark.

_`Wildcard Part`
    ``m.connect('file/`` \*url ``', controller='file', action='serve')``
    
    A wildcard part will match *everything* except the other parts around it.

_`Groupings`
    ``m.connect('article', 'article/:section/:slug/`` :(page) ``.html', ...``
    
    ``m.connect('file/`` \*(url) ``.html', controller='file', action='serve')``
    
    Groupings let you define boundaries for the match with the () characters.
    This allows you to match wildcards and dynamics next to other static and
    dynamic parts. Care should be taken when using Groupings next to each other.
    

Defaults
--------

*Optional* 

    ``m.connect('history', 'archives/by_eon/:century',``
    controller='archives', action='aggregate', century=1800 ``)``

The keyword options in a route (not including the `requirements`_ keyword arg)
that can determine the default for a route. If a default is specified for a
variable that is not a `dynamic part`_, then its not only a default but is also
a *hardcoded variable*. The ``controller`` and ``action`` are hardcoded
variables in the example above because despite the URL, they will always be
'archives' and 'aggregate' respectively.

_`Hardcoded Variable`
    Default keyword that does not exist in the `route path`_. This keyword
    variable cannot be changed by the URL coming in.

Requirements
------------

*Optional*

    ``m.connect('archives/:year/:month/:day', controller='archives', action='view', year=2004,``
    requirements=dict(year='\d{2,4}', month='\d{1,2}') ``)``

Requirements is a special keyword used by Routes to enforce a regular
expression restriction on the `dynamic part`_ or `wildcard part`_ of a
`route path`_.

Conditions
----------

*Optional*
    
    ``m.connect('user/new;preview', controller='user', action='preview',``
    conditions=dict(method=['POST']) ``)``

Conditions specifies a set of special conditions that must be met for the 
route to be accepted as a valid match for the URL. The conditions argument must
always be a dictionary and can accept 3 different keys.

``method``
    Request must be one of the HTTP methods defined here. This argument must be
    a list of HTTP methods, and should be upper-case.
``sub_domain``
    Can either be ``True`` or a Python list of sub-domains, one of which must
    be present.
``function``
    A function that will be used to evaluate if the Route is a match. Must
    return True or False, and will be called with the ``environ`` and
    ``match_dict``. The ``match_dict`` is a dict with all the Route variables
    for the request. Modifications to ``match_dict`` will appear identical to
    Route variables from the original match.

Examples:

.. code-block:: python
    
    # The method to be either GET or HEAD
    m.connect('user/list', controller='user', action='list',
              conditions=dict(method=['GET', 'HEAD']))
    
    
    # A sub-domain should be present
    m.connect('', controller='user', action='home',
              conditions=dict(sub_domain=True))
    
    # Sub-domain should be either 'fred' or 'george'
    m.connect('', controller='user', action='home',
              conditions=dict(sub_domain=['fred', 'george']))
    
    
    # Put the referrer into the resulting match dictionary, this won't stop the match
    # since it always returns True
    def referals(environ, result):
        result['referer'] = environ.get('HTTP_REFERER')
        return True
    m.connect(':controller/:action/:id', conditions=dict(function=referals))


-------------------------------
The Nitty Gritty of Route Setup
-------------------------------

Minimum URLs
------------

Routes will use your `defaults`_ to try and minimize the required length of
your URL whenever possible. For example:

.. code-block:: python
    
    m.connect(':controller/:action/:id', action='view', id=4)
    
    # Will match all of the following
    # /content/view/4
    # /content/view
    # /content

Trailing `dynamic parts <#dynamic-part>`_ of a `route path`_ that have
`defaults`_ setup are not required to exist in the URL being matched. This 
means that each of the URL examples shown above will result in the same set of
keyword arguments being sent to the same controller and action.

If a `dynamic part`_ with a default is followed by either 
`static parts <#static-part>`_ or `dynamic parts <#dynamic-part>`_ without 
`defaults`_, that `dynamic part`_ will be required despite having a default:

.. code-block:: python

    # Remember that :action has an implicit default
    m.connect('archives/:action/:article', controller='blog')
    
    # Matches:
    # /archives/view/introduction
    # /archives/edit/recipes
    
    # Does Not Match:
    # /archives/introduction
    # /archives/recipes
    
This way, the URL coming in maps up to the `route path`_ you created, part
for part.

When using `Groupings`_, parts will still be left off, but only if the
remainder of the URL has no static after it. This can lead to some odd looking
URLs being generated if you aren't careful about your requirements and 
defaults. For example:

.. code-block:: python

    # Groupings without requirements
    m.connect(':controller/:(action)-:(id)')
    
    # Matches:
    # /archives/view-3
    # /archives/view-
    
    # Generation:
    url_for(controller='archives', action='view')
    # /archives/view-

It's unlikely you want such a URL, and would prefer to ensure that there's
always an id supplied. To enforce this behavior we will use `Requirements`_:

.. code-block:: python

    # Groupings without requirements
    m.connect(':controller/:(action)-:(id)', requirements=dict(id='\d+'))
    
    # Matches:
    # /archives/view-3
    # /archives/view-2
    
    # Does Not Match:
    # /archives/view-
    
    # Generation:
    url_for(controller='archives', action='view', id=2)
    # /archives/view-2

If you end up with URLs missing parts you'd like left on when using
`Groupings`_, add a requirement to that part.

Implicit Defaults
-----------------

The above rule regarding `minimum URLs`_ has two built-in implicit `defaults`_.
If you use either ``action`` or ``id`` in your `route path`_ and don't specify
`defaults`_ for them, Routes will automatically assign the following defaults
to them for you:

.. code-block:: python

    action='index', id=None
    
This is why using the following setup doesn't require an action or id in the
URL:

.. code-block:: python

    m.connect(':controller/:action/:id')
    
    # '/blog'  -> controller='blog', action='index', id=None
    
Search Order
------------

When setting up your routes, remember that when `using routes`_ the order in
which you set them up can affect the URL that's generated. Routes will try and
use all the keyword args during route generation and if multiple routes can be
generated given the set of keyword args, the **first and shortest route that
was connected to the mapper will be used**. `Hardcoded variables 
<#hardcoded-variable>`_ are also used first if available as they typically 
result in shorter URLs.

For example:

.. code-block:: python

    # Route Setup
    m.connect('archives/:year', controller='blog', action='view', year=None)
    m.connect(':controller/:action/:id')
    
    # Route Usage
    url_for(controller='blog', action='view')      ->        '/archives'
    
You will typically want your specific and detailed routes at the top of your
Route setup and the more generic routes at the bottom.

Wildcard Limitations and Gotchas
--------------------------------

Due to the nature of `wildcard parts <#wildcard-part>`_, using wildcards in
your route path can result in URL matches that you didn't expect. `Wildcard 
parts <#wildcard-part>`_ are extremely powerful and when combined with 
`dynamic parts <#dynamic-part>`_  that have `defaults`_ can confuse the new 
Routes user.

When you have `dynamic parts <#dynamic-part>`_ with `defaults`_, you should 
never place them directly next to a `wildcard part`_. This can result in the
`wildcard part`_ eating the part in the URL that was intended as the
`dynamic part`_. 

For example:

.. code-block:: python

    m.connect('*url/:username', controller='blog', action='view', username='george')
    
    # When matching                        url variable              username variable
    # /some/long/url/george                /some/long/url/george     george
    # /some/other/stuff/fred               /some/other/stuff/fred    george
    
This occurs because Routes sees the default as being optional, and the 
`wildcard part`_ attempts to gobble as much of the URL as possible before a 
required section of the `route path`_ is found. By having a trailing
`dynamic part`_ with a default, that section gets dropped.

Notice how removing the `dynamic part`_ default results in the variables we 
expect:

.. code-block:: python

    m.connect('*url/:username', controller='blog', action='view')

    # When matching                        url variable              username variable
    # /some/long/url/george                /some/long/url            george
    # /some/other/stuff/fred               /some/other/stuff         fred

Let's try one more time, but put in a `static part`_ between the 
`dynamic part`_ with a default and the wildcard:

.. code-block:: python

    m.connect('*url/user/:username', controller='blog', action='view', username='george')

    # When matching                        url variable              username variable
    # /some/long/url/user/george           /some/long/url            george
    # /some/other/stuff/user/fred          /some/other/stuff         fred

Unicode
-------

Routes by default will assume that incoming parameters are UTF-8 encoded and 
handle the appropriate encoding/decoding. This means that *all* route variables
will be unicode objects. Should you wish to change the encoding or turn it off
altogether:

.. code-block:: python
    
    map = Mapper()
    map.encoding = None # defaults to 'utf-8'
    
    map.connect(':controller/:action/:id')

Individual routes can have their encoding options toggled as well, should a
specific route want an raw string from the browser. Just add the ``_encoding`` 
option to the route:

.. code-block:: python
    
    map = Mapper()
    
    map.connect('myapp', controller='myapp', action='wsgi', _encoding=None)
    map.connect(':controller/:action/:id')

------------
Using Routes
------------

Once you have setup the Routes to map URLs to your controllers and actions, you
will likely want to generate URLs from within your web application. Routes
includes two functions for use in your web application that are commonly 
desired.

* `redirect_to <module-routes.html#redirect_to>`_
* `url_for <module-routes.html#url_for>`_

Both of these functions take a similar set of arguments. The most important
being a set of keyword arguments that describes the controller, action, and
additional variables you'd like present for the URL that's created.

To save you from repeating things, Routes has two mechanisms to reduce the
amount of information you need to supply the url_for or redirect_to function.

Named Routes
------------

We saw earlier how the `route name`_ ties a set of `defaults`_ to a name. We
can use this name with our Route functions and its as if we used that set of
keyword args:

.. code-block:: python

    m.connect('category_home', 'category/:section', controller='blog', action='view',
              section='home')
    
    url_for('category_home')
    # is equivalent to
    url_for(controller='blog', action='view', section='home')
    
You can also specify keyword arguments and it will override `defaults`_ associated with the `route name`_:

.. code-block:: python

    url_for('category_home', action='index')
    #is equivalent to
    url_for(controller='blog', action='index', section='home')
    
As you can see, the amount of typing you save yourself by using the `route 
name`_ feature is quite handy.

Using the recently introduced `static named routes`_ feature allows you to 
quickly use common URLs and easily add query arguments:

.. code-block:: python

    m.connect('google_search', 'http://www.google.com/search', _static=True)
    
    url_for('google_search', q='routes')
    # will result in
    # http://www.google.com/search?q=routes

Non-Existent Route Names
^^^^^^^^^^^^^^^^^^^^^^^^

If you supply a `route name`_ that does not exist, ``url_for`` will assume that
you intend to use the name as the actual URL. It will also prepend it with the
proper WSGI ``SCRIPT_NAME`` if applicable:

.. code-block:: python

    url_for('/css/source.css')
    # if running underneath a 'mount' point of /myapp will become
    # /myapp/css/source.css

For portable web applications, it's highly encouraged that you use ``url_for`` 
for all your URLs, even those that are static resources and images. This will 
ensure that the URLs are properly handled in various deployment cases.

Route Memory
------------

When your controller and action is matched up from the URL, the variables it 
set to get there are preserved. This lets you update small bits of the keywords
that got you there without specifying the entire thing:

.. code-block:: python

    m.connect('archives/:year/:month/:day', controller='archives',
              action='view', year=2004,
              requirements=dict(year='\d{2,4}', month='\d{1,2}'))

    # URL used: /archives/2005/10/4
    
    # Route dict: {'controller': 'archives', 'action': 'view', 'year': '2005',
    #              'month': '10', 'day': '4'}
    
    url_for(day=6)                     # =>          /archives/2005/10/6
    url_for(month=4)                   # =>          /archives/2005/4/4
    url_for()                          # =>          /archives/2005/10/4
    url_for(controller='/archives')    # =>          /archives
    
The route memory is always used for values with the following conditions:

* If the controller name begins with a ``/``, no values from the Route dict 
  are used
* If the controller name changes and no action is specified, action will be set
  to 'index'
* If you use `named routes`_, no values from the Route dict are used

Overriding Route Memory
-----------------------

Sometimes one doesn't want to have `Route Memory`_ present, as well as removing
the `Implicit Defaults`_. Routes can disable route memory and implicit defaults
either globally, or on a per-route basis. Setting explicit routes:

.. code-block:: python
    
    m = Mapper(explicit=True)

When toggling explicit behavior for individual routes, only the implicit route
defaults will be de-activated. ``url_for`` behavior can only be set globally 
with the mapper explicit keyword. Setting explicit behavior for a route:

.. code-block:: python
    
    m = Mapper()
    
    # Note no 'id' value will be assumed for a default
    m.connect('archives/:year', controller='archives', action='view',
              _explicit=True)
    
    # This will now require an action and id present
    m.connect(':controller/:action/:id', _explicit=True)

------------------
Sub-domain Support
------------------

Routes comes with sub-domain support to make it easy to handle sub-domains in
an integrated fashion. When sub-domain support is turned on, Routes will always
have a ``sub_domain`` argument present with the sub-domain if present, or None.

To avoid matching common aliases to your main domain like ``www``, the 
sub-domain support can be set to ignore some sub-domains.

Example:

.. code-block:: python
    
    # Turn on sub-domain support
    map.sub_domains = True
    
    # Ignore the www sub-domain
    map.sub_domains_ignore = ['www']

Generating URL's with sub-domains
---------------------------------

When sub-domain support is on, the ``url_for`` function will accept a 
``sub_domain`` keyword argument. Routes will then ensure that the generated URL
has the sub-domain indicated. This feature works with Route memory to ensure
that the sub-domain is only added when necessary.

Some examples:

.. code-block:: python
    
    # Assuming that the current URL from the request is http://george.example.com/users/edit
    # Also assuming that you're using the map options above with the default routing of
    # ':controller/:action/:id'
    url_for(action='update', sub_domain='fred')   # -> http://fred.example.com/users/update
    
    url_for(controller='/content', action='view', sub_domain='www')
    # will become -> http://example.com/content/view
    
    url_for(action='new', sub_domain=None)        # -> http://example.com/users/new

----------------
RESTful Services
----------------

To make it easier to setup RESTful web services with Routes, there's a shortcut
Mapper method that will setup a batch of routes for you along with conditions
that will restrict them to specific HTTP methods. This is directly styled on
the Rails version of ``map.resource``, which was based heavily on the Atom
Publishing Protocol.

The ``map.resource`` command creates a set of Routes for common operations on
a collection of resources, individually referred to as 'members'. Consider the
common case where you have a system that deals with users. In that case
operations dealing with the entire group of users (or perhaps a subset) would
be considered *collection* methods. Operations (or actions) that act on an
individual member of that collection are considered *member* methods. These
terms are important to remember as the options to ``map.resource`` rely on a
clear understanding of *collection* actions vs. *member* actions.

View a `complete list with examples of the map.resource options <class-routes.base.Mapper.html#resource>`_.

The default mapping that map.resource sets up looks like this:

.. code-block:: python
    
    map.resource('message', 'messages')
    
    # Will setup all the routes as if you had typed the following map commands:
    map.connect('messages', controller='messages', action='create', 
        conditions=dict(method=['POST']))
    map.connect('messages', 'messages', controller='messages', action='index',
        conditions=dict(method=['GET']))
    map.connect('formatted_messages', 'messages.:(format)', controller='messages', action='index',
        conditions=dict(method=['GET']))
    map.connect('new_message', 'messages/new', controller='messages', action='new',
        conditions=dict(method=['GET']))
    map.connect('formatted_new_message', 'messages/new.:(format)', controller='messages', action='new',
        conditions=dict(method=['GET']))
    map.connect('messages/:id', controller='messages', action='update',
        conditions=dict(method=['PUT']))
    map.connect('messages/:id', controller='messages', action='delete',
        conditions=dict(method=['DELETE']))
    map.connect('edit_message', 'messages/:(id);edit', controller='messages, action='edit',
        conditions=dict(method=[''GET']))
    map.connect('formatted_edit_message', 'messages/:(id).:(format);edit', controller='messages, 
        action='edit', conditions=dict(method=[''GET']))
    map.connect('message', 'messages/:id', controller='messages', action='show',
        conditions=dict(method=['GET']))
    map.connect('formatted_message', 'messages/:(id).:(format)', controller='messages', action='show',
        conditions=dict(method=['GET']))

The most important aspects of this is the following mapping that is established::
    
    GET    /messages         -> messages.index()          -> url_for('messages')
    POST   /messages         -> messages.create()         -> url_for('messages')
    GET    /messages/new     -> messages.new()            -> url_for('new_message')
    PUT    /messages/1       -> messages.update(id)       -> url_for('message', id=1)
    DELETE /messages/1       -> messages.delete(id)       -> url_for('message', id=1)
    GET    /messages/1       -> messages.show(id)         -> url_for('message', id=1)
    GET    /messages/1;edit  -> messages.edit(id)         -> url_for('edit_message', id=1)

.. note::

    Several of these methods map to functions intended to display forms. The
    new message method should be used to return a form allowing someone to 
    create a new message, while it should POST to /messages. The edit message
    function should work similarly returning a form to edit a message, which
    then posts a PUT to the /messages/1 resource.

Additional methods that respond to either a new member, or different ways of 
viewing collections can be added via keyword arguments to ``map.resource`` as
shown in the `complete list with examples of the map.resource options 
<class-routes.base.Mapper.html#resource>`_.

--------------------
Additional Resources
--------------------

*These resources may refer to Ruby/Rails route setup*

* `Rails Routes book <http://manuals.rubyonrails.com/read/book/9>`_
* `Rails Named Routes How-To <http://wiki.rubyonrails.com/rails/pages/NamedRoutes>`_

.. _quickwiki_tutorial:

.. quickwiki-tutorial:

==================
Quickwiki tutorial
==================

Introduction 
============ 

If you haven't done so already, please first read the :ref:`getting_started` guide. 

In this tutorial we are going to create a working wiki from scratch using Pylons 0.9.7 and SQLAlchemy. Our wiki will allow visitors to add, edit or delete formatted wiki pages. 

Starting at the End 
=================== 

Pylons is designed to be easy for everyone, not just developers, so let's start by downloading and installing the finished QuickWiki in exactly the same way that end users of QuickWiki might do. Once we have explored its features we will set about writing it from scratch.

After you have installed `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ run these commands to install QuickWiki and create a config file: 

.. code-block :: bash 

    $ easy_install QuickWiki==0.1.6 
    $ paster make-config QuickWiki test.ini 

Next, ensure that the ``sqlalchemy.url`` variable in the ``[app:main]`` section of the configuration file (``development.ini``) specifies a value that is suitable for your setup. The data source name points to the database you wish to use. 

.. note :: 

    The default ``sqlite:///%(here)s/quickwiki.db`` uses a (file-based) SQLite database named ``quickwiki.db`` in the ini's top-level directory. This SQLite database will be created for you when running the ``paster setup-app`` command below, but you could also use MySQL, Oracle or PostgreSQL. Firebird and MS-SQL may also work. See the `SQLAlchemy documentation <http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_establishing>`_ for more information on how to connect to different databases. SQLite for example requires additional forward slashes in its URI, where the client/server databases should only use two. You will also need to make sure you have the appropriate Python driver for the database you wish to use. If you're using Python 2.5, a version of the `pysqlite adapter <http://www.initd.org/tracker/pysqlite/wiki/pysqlite>`_ is already included, so you can jump right in with the tutorial. You may need to get `SQLite itself <http://www.sqlite.org/download.html>`_. 

Finally create the database tables and serve the finished application: 

.. code-block :: bash 

    $ paster setup-app test.ini 
    $ paster serve test.ini 

That's it! Now you can visit ``http://127.0.0.1:5000`` and experiment with the finished Wiki. 

When you've finished, stop the server with ``CTRL+C`` because we will start developing our own version. 

If you are interested in looking at the latest version of the QuickWiki source code it can be browsed online at http://www.knowledgetap.com/hg/QuickWiki or can be checked out using Mercurial: 

.. code-block :: bash 

    $ hg clone http://www.knowledgetap.com/hg/QuickWiki 

.. note :: 

    To run the version checked out from the repository, you'll want to run ``python setup.py egg_info`` from the project's root directory. This will generate some files in the ``QuickWiki.egg-info`` directory.

Developing QuickWiki 
==================== 

If you skipped the "Starting at the End" section you will need to assure yourself that you have Pylons installed. See the :ref:`getting_started`.

Then create your project: 

.. code-block :: bash 

    $ paster create -t pylons QuickWiki

When prompted for which templating engine to use, simply hit enter for the default (Mako). When prompted for SQLAlchemy configuration, enter 'True'.

Now let's start the server and see what we have: 

.. code-block :: bash 

    $ cd QuickWiki 
    $ paster serve --reload development.ini 

.. note :: We have started the server with the ``--reload`` switch. This means any changes that we make to code will cause the server to restart (if necessary); your changes are immediately reflected on the live site. 

Visit ``http://127.0.0.1:5000`` where you will see the introduction page. Now delete the file :file:`public/index.html` because we want to see the front page of the wiki instead of this welcome page. If you now refresh the page, the Pylons built-in error document support will kick in and display an ``Error 404`` page to tell you the file could not be found. We'll setup a controller to handle this location later. 


The Model 
========= 

Pylons uses a Model-View-Controller architecture; we'll start by creating the model. We could use any system we like for the model, including `SQLAlchemy <http://www.sqlalchemy.org>`_ or `SQLObject <http://www.sqlobject.org>`_. Optional SQLAlchemy integration is provided for new Pylons projects, so we'll use it for QuickWiki. 

.. note :: SQLAlchemy is a powerful Python SQL toolkit and Object Relational Mapper that is popular with many Python programmers. 

SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performance database access, adapted into a simple and Pythonic domain language. It has full and detailed documentation available on the SQLAlchemy website: http://sqlalchemy.org/docs/.

The most basic way of using SQLAlchemy is with explicit sessions where you create ``Session`` objects as needed. 

Pylons applications typically employ a slightly more sophisticated setup, using SQLAlchemy's "contextual" thread-local sessions via :meth:`scoped_session`. With this configuration, the application can use a single :class:`Session` instance per web request, avoiding the need to pass it around explicitly. Instantiating a new :class:`Session` will actually find an existing one in the current thread if available. There are further details in the `SQLAlchemy documentation on the Session <http://www.sqlalchemy.org/docs/04/session.html#unitofwork_contextual>`_. 

.. note :: It is important to recognize the difference between SQLAlchemy's (or possibly another DB abstraction layer's) :class:`Session` object and Pylons' standard :dfn:`session` (with a lowercase 's') for web requests. See :mod:`beaker` for more on the latter. It is customary to reference the database session by :class:`model.Session` or (more recently) ``Session`` outside of model classes. 

The default imports already present in :file:`model/__init__.py` provide some SQLAlchemy objects such as the :mod:`sqlalchemy` module (aliased as :mod:`sa`) as well as the ``metadata`` object. ``metadata`` is used when defining and managing tables. Now we take advantage of that and add the following to the end of the contents of the :file:`model/__init__.py` file: 

.. code-block :: python 
    
    pages_table = sa.Table('pages', meta.metadata, 
                    sa.Column('title', sa.types.Unicode(40), primary_key=True), 
                    sa.Column('content', sa.types.Unicode(), default='') 
                    )
    
    class Page(object):
        pass

    orm.mapper(Page, pages_table)

We now define a table called ``pages`` which has two columns, ``title`` (the primary key) and ``content``. 

.. note :: 
    SQLAlchemy also supports reflecting table information directly from a database. If we had already created the ``pages`` database table, SQLAlchemy could have constructed the ``pages_table`` object for us. This uses the ``autoload=True`` parameter in place of the ``Column`` definitions, like this: 

.. code-block :: python 

    pages_table = sa.Table('pages', metadata, autoload=True) 

`SQLAlchemy table reflection documentation <http://www.sqlalchemy.org/docs/04/metadata.html#metadata_tables_reflecting>`_ 

.. note :: A primary key is a unique ID for each row in a database table. In the example above we are using the page title as a natural primary key. Some people prefer to use integer primary keys for all tables, so-called surrogate primary keys. The author of this tutorial uses both methods in his own code and is not advocating one method over the other, it is important that you choose the best database structure for your application. See the Pylons Cookbook for `a quick general overview of relational databases <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_ if you're not familiar with these concepts. 

A core philosophy of SQLAlchemy is that tables and domain classes are different beasts. So next, we'll create the Python class that will represent the pages of our wiki and map these domain objects to rows in the ``pages`` table using a mapper. In a more complex application, you could break out model classes into separate ``.py`` files in your ``model`` directory, but for sake of simplicity in this case, we'll just stick to :file:`__init__.py`. 

Add this to the bottom of ``model/__init__.py``: 

.. code-block :: python 

    class Page(object): 

        def __unicode__(self):
            return self.title

        __str__ = __unicode__

    orm.mapper(Page, pages_table) 

.. note :: For those more familiar with SQLAlchemy 0.3: in SQLAlchemy versions 0.4 and 0.5 :func:`scoped_session` replaces the :func:`sessioncontext` extension and so :class:`Session.mapper` could be used here in place of
 :func:`orm.mapper` to get behavior similar to that achieved with :func:`assign_mapper`. This is considered to be an advanced topic and you should consult SQLAlchemy's documentation if you wish to learn how it works. 

Looking ahead, our wiki will need some formatting so we will need to turn the ``content`` field into HTML. Any "WikiWords" (words made by joining together two or more lowercase words with the first letter capitalized) will also need to be converted into hyperlinks. 

It would be advantageous if we could add a method to our :class:`Page` object to retrieve the formatted HTML with the WikiWords already converted to hyperlinks. Add the following at the top of the :file:`model/__init__.py` file: 

.. code-block :: python 

    import logging
    import re
    import sets
    from docutils.core import publish_parts

    from pylons import url
    from quickwiki.lib.helpers import link_to
    from quickwiki.model import meta

    log = logging.getLogger(__name__)

    SAFE_DOCUTILS = {'file_insertion_enabled': False, 'raw_enabled': False}
    wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE)

and then add a :meth:`get_wiki_content` method to the ``Page`` object so it looks like this: 

.. code-block :: python 

    class Page(object):
        def __init__(self, title, content=None):
            self.title = title
            self.content = content

        def get_wiki_content(self):
            """Convert reStructuredText content to HTML for display, and
            create links for WikiWords.
            """
            content = publish_parts(self.content, writer_name='html',
                                    settings_overrides=SAFE_DOCUTILS)['html_body']
            titles = sets.Set(wikiwords.findall(content))
            for title in titles:
                title_url = url(controller='pages', action='show', title=title)
                content = content.replace(title, link_to(title, title_url))
            return content


This code deserves a bit of explaining. The ``content = None`` line is so that the ``content`` attribute is initialized to ``None`` when a new :class:`Page` object is created. The :class:`Page` object represents a row in the ``pages`` table so ``self.content`` will be the value of the ``content`` field. The :class:`Set` object provides us with only unique WikiWord names, so we don't try replacing them more than once (a "wikiword" is of course defined by the regular expression set globally). 

.. note :: 

    Pylons uses a **Model View Controller** architecture and so the formatting of objects into HTML should  properly be handled in the View, i.e. in a template. In this example however, converting reStructuredText into HTML in a template is inappropriate so we are treating the HTML representation of the content as part of the model. It also gives us the chance to demonstrate that SQLAlchemy domain classes are real Python classes that can have their own methods. 

The :func:`link_to` and :func:`url` functions referenced in the controller code are respectively: a helper imported from :file:`webhelpers.html` indirectly via :file:`lib/helpers.py` and a utility function imported directly from the Pylons module. They both act as ``helper`` utilities for creating links to specific controller actions. In this case we have decided that all WikiWords should link to the :meth:`index` action of the ``page`` controller which we will create later. However, we need to ensure that the :func:`link_to` function is made available as a helper by adding an import statement to :file:`lib/helpers.py`:

.. code-block :: python

    """Helper functions

    Consists of functions to typically be used within templates, but also
    available to Controllers. This module is available to templates as 'h'.
    """
    from webhelpers.html.tags import *

One final change; since we have used docutils and SQLAlchemy, both third party packages, we need to edit our :file:`setup.py` file so that anyone installing QuickWiki with `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ will automatically also have these dependencies installed for them too. Edit your :file:`setup.py` in your project root directory so that the ``install_requires`` line looks like this: 

.. code-block :: python 

    install_requires=["Pylons>=0.9.7", "docutils==0.4", "SQLAlchemy>=0.5"], 

While we are we are making changes to :file:`setup.py` we might want to complete some of the other sections too. Set the version number to 0.1.6 and add a description and URL which will be used on PyPi when we release it: 

.. code-block :: python 

    version='0.1.6', 
    description='QuickWiki - Pylons 0.9.7 Tutorial application', 
    url='http://docs.pylonshq.com/tutorials/quickwiki_tutorial.html', 

We might also want to make a full release rather than a development release in which case we would remove the following lines from :file:`setup.cfg`: 

.. code-block :: ini 

    [egg_info] 
    tag_build = dev 
    tag_svn_revision = true 

To test the automatic installation of the dependencies, run the following command which will also install docutils and SQLAlchemy if you don't already have them: 

.. code-block :: bash 

    $ python setup.py develop 

.. note :: 

    The command ``python setup.py develop`` installs your application in a special mode so that it behaves exactly as if it had been installed as an egg file by an end user. This is really useful when you are developing an application because it saves you having to create an egg and install it every time you want to test a change. 

Application Setup 
=================

Edit ``websetup.py``, used by the ``paster setup-app`` command, to look like this: 

.. code-block :: python 

    """Setup the QuickWiki application"""
    import logging

    from quickwiki.config.environment import load_environment

    log = logging.getLogger(__name__)

    def setup_app(command, conf, vars):
        """Place any commands to setup quickwiki here"""
        load_environment(conf.global_conf, conf.local_conf)

        # import model now that the environment is loaded
        from quickwiki import model
        from quickwiki.model import meta
        meta.metadata.bind = meta.engine

        # Create the tables if they aren't there already
        log.info("Creating tables...")
        meta.metadata.create_all(checkfirst=True)
        log.info("Successfully set up.")

        log.info("Adding front page data...")
        page = model.Page(title=u'FrontPage',
                          content=u'Welcome to the QuickWiki front page.')
        meta.Session.add(page)
        meta.Session.commit()
        log.info("Successfully set up.")


You can see that :file:`config/environment.py`'s :func:`load_environment` function is called, so our engine is ready for binding and we can import the model. A SQLAlchemy :class:`MetaData` object -- which provides some utility methods for operating on database schema -- usually needs to be connected to an engine, so the line  

.. code-block :: python

    meta.metadata.bind = meta.engine

does exactly that and then

.. code-block :: python

    model.metadata.create_all(checkfirst=True)

uses the connection we've just set up and, well, creates the table(s) we've defined ... if they don't already exist. After the tables are created, the other lines add some data for the simple front page to our wiki.

By default, SQLAlchemy specifies ``autocommit=False`` when creating the ``Session``, which means that operations will be wrapped in a transaction and committed atomically (unless your DB doesn't support transactions, like MySQL's default MyISAM tables -- but that's beyond the scope of this tutorial). 

To test this functionality run you first need to install your QuickWiki if you haven't already done so in order for ``paster`` to find the version we are developing instead of the version we installed at the very start: 

.. code-block :: bash 

    $ python setup.py develop 

Specify your database URI in :file:`development.ini` so that the ``[app:main]`` section contains something like this, customized as needed for your database: 

.. code-block :: ini

    [app:main] 
    use = egg:QuickWiki 
    #... 
    # Specify the database for SQLAlchemy to use. 
    # %(here) may include a ':' character on Windows environments; this can 
    # invalidate the URI when specifying a SQLite db via path name 
    sqlalchemy.url = sqlite:///%(here)s/quickwiki.db 

.. note :: 

    See the SQLAlchemy note in the `Starting at the End`_ section for information on supported database URIs and a link to the SQLAlchemy documentation about the various options that can be included in them. 

If you want to see the SQL being generated, you can have SQLAlchemy echo it to the console by adding this line: 

.. code-block :: ini 

    sqlalchemy.echo = true 

You can now run the ``paster setup-app`` command to setup your tables in the same way an end user would, remembering to drop and recreate the database if the version tested earlier has already created the tables: 

.. code-block :: bash 

    $ paster setup-app development.ini 

At this stage you will need to ensure you have the appropriate Python database drivers for the database you chose, otherwise you might find SQLAlchemy complains it can't get the DBAPI module for the dialect it needs. 

You should also edit :file:`quickwiki/config/deployment.ini_tmpl` so that when users run ``paster make-config`` the configuration file that is produced for them will already have a section telling them to enter their own database URI as we did when we installed the finished QuickWiki at the start of the tutorial. Add these lines in the ``[app:main]`` section: 

.. code-block :: ini 

    # Specify the database for SQLAlchemy to use. 
    # %(here) may include a ':' character on Windows environments; this can 
    # invalidate the URI when specifying a SQLite db via path name 
    sqlalchemy.url = sqlite:///%(here)s/quickwiki.db 

Templates 
========= 

.. note :: 

    Pylons uses the Mako templating language by default, although as is the case with most aspects of Pylons, you are free to deviate from the default if you prefer.

In our project we will make use of a feature of the Mako templating language called "inheritance". Add the main page template in :file:`templates/base.mako`: 

.. code-block :: html+mako 

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html>
      <head>
        <title>QuickWiki</title>
        ${h.stylesheet_link('/quick.css')}
      </head>

      <body>
        <div class="content">
          <h1 class="main">${self.header()}</h1>
          ${next.body()}\
          <p class="footer"> 
              Return to the 
              ${h.link_to('FrontPage', 
                  url(action="index", title="FrontPage"))} 
              | ${h.link_to('Edit ' + c.title, 
                  url(title=c.title, action='edit'))} 
          </p> 
        </div>
      </body>
    </html>

We'll setup all our other templates to inherit from this one: they will be automatically inserted into the ``${next.body()}`` line. Thus the whole page will be returned when we call the :func:`render` global from our controller. This lets us easily apply a consistent theme to all our templates. 

If you are interested in learning some of the features of Mako templates have a look at the comprehensive `Mako Documentation <http://www.makotemplates.org/docs/>`_. For now we just need to understand that :func:`next.body` is replaced with the child template and that anything within ``${...}`` brackets is executed and replaced with the result. By default, the replacement content is HTML-escaped in order to meet modern standards of basic protection from accidentally making the app vulnerable to XSS exploit.

This :file:`base.mako` also makes use of various helper functions attached to the ``h`` object. These are described in the `WebHelpers documentation <http://pylonshq.com/WebHelpers/module-index.html>`_. We need to add some helpers to the ``h`` by importing them in the :file:`lib/helpers.py` module (some are for later use):

.. code-block :: python

    """Helper functions

    Consists of functions to typically be used within templates, but also
    available to Controllers. This module is available to templates as 'h'.
    """
    from webhelpers.html import literal
    from webhelpers.html.tags import *
    from webhelpers.html.secure_form import secure_form
 

Note that the :file:`helpers` module is available to templates as 'h', this is a good place to import or define directly any convenience functions that you want to make available to all templates. 

Routing 
======= 

Before we can add the actions we want to be able to route the requests to them correctly. Edit :file:`config/routing.py` and adjust the 'Custom Routes' section to look like this: 

.. code-block :: python 

    # CUSTOM ROUTES HERE

    map.connect('home', '/', controller='pages', action='show',
                title='FrontPage')
    map.connect('pages', '/pages', controller='pages', action='index')
    map.connect('show_page', '/pages/show/{title}', controller='pages',
                action='show')
    map.connect('edit_page', '/pages/edit/{title}', controller='pages',
                action='edit')
    map.connect('save_page', '/pages/save/{title}', controller='pages',
                action='save', conditions=dict(method='POST'))
    map.connect('delete_page', '/pages/delete/{title}', controller='pages',
                action='delete')

    # A bonus example - the specified defaults allow visiting
    # example.com/FrontPage to view the page titled 'FrontPage':
    map.connect('/{title}', controller='pages', action='show')

    return map

Note that the default route has been replaced. This tells Pylons to route the root URL ``/`` to the :meth:`show()` method of the :class:`PageController` class in :file:`controllers/pages.py` and specify the ``title`` argument as ``'FrontPage'``. It also says that any URL of the form ``/SomePage`` should be routed to the same method but the ``title`` argument will contain the value of the first part of the URL, in this case ``SomePage``. Any other URLs that can't be matched by these maps are routed to the error controller as usual where they will result in a 404 error page being displayed. 

One of the main benefits of using the Routes system is that you can also create URLs automatically, simply by specifying the routing arguments. For example if I want the URL for the page ``FrontPage`` I can create it with this code: 

.. code-block :: python 

    url(title='FrontPage') 

Although the URL would be fairly simple to create manually, with complicated URLs this approach is much quicker. It also has the significant advantage that if you ever deploy your Pylons application at a URL other than ``/``, all the URLs will be automatically adjusted for the new path without you needing to make any manual modifications. This flexibility is a real advantage. 

Full information on the powerful things you can do to route requests to controllers and actions can be found in the `Routes manual <http://routes.groovie.org/manual.html>`_. 

Controllers 
=========== 

Quick Recap: We've setup the model, configured the application, added the routes and setup the base template in :file:`base.mako`, now we need to write the application logic and we do this with controllers. In your project's root directory, add a controller called ``pages`` to your project with this command: 

.. code-block :: bash 

    $ paster controller pages

If you are using Subversion, this will automatically be detected and the new controller and tests will be automatically added to your subversion repository.

We are going to need the following actions: 

``show(self, title)``
displays a page based on the title 

``edit(self, title)`` 
displays a from for editing the page ``title`` 

``save(self, title)`` 
save the page ``title`` and show it with a saved message 

``index(self)`` 
lists all of the titles of the pages in the database

``delete(self, title)`` 
deletes a page

:meth:`show` 
--------------- 

Let's get to work on the new controller in :file:`controllers/pages.py`. First we'll import the :class:`Page` class from our :mod:`model`, and the :class:`Session` class from the :mod:`model.meta` module. We'll also import the ``wikiwords`` regular expression object, which we'll use in the :meth:`show` method. Add this line with the imports at the top of the file: 

.. code-block :: python 

    from quickwiki.model import Page, wikiwords
    from quickwiki.model.meta import Session

Next we'll add the convenience method :meth:`__before__` to the :class:`PagesController`, which is a special method Pylons always calls before calling the actual action method. We'll have :meth:`__before__` obtain and make available the relevant query object from the database, ready to be queried. Our other action methods will need this query object, so we might as well create it one place.

.. code-block :: python 

    class PagesController(BaseController):

        def __before__(self):
            self.page_q = Session.query(Page)

Now we can query the database using the query expression language provided by SQLAlchemy.
Add the following :meth:`show` method to :class:`PagesController`:

.. code-block :: python 

    def show(self, title):
        page = self.page_q.filter_by(title=title).first()
        if page:
            c.content = page.get_wiki_content()
            return render('/pages/show.mako')
        elif wikiwords.match(title):
            return render('/pages/new.mako')
        abort(404)

Add a template called :file:`templates/pages/show.mako` that looks like this: 

.. code-block :: html+mako 

    <%inherit file="/base.mako"/>\

    <%def name="header()">${c.title}</%def>

    ${h.literal(c.content)}

This template simply displays the page title and content. 

.. note :: Pylons automatically assigns all the action parameters to the Pylons context object ``c`` so that you don't have to assign them yourself. In this case, the value of ``title`` will be automatically assigned to ``c.title`` so that it can be used in the templates. We assign ``c.content`` manually in the controller. 

We also need a template for pages that don't already exist. The template needs to display a message and link to the :meth:`edit` action so that they can be created. Add a template called :file:`templates/new.mako` that looks like this: 

.. code-block :: html+mako 

    <%inherit file="/base.mako"/>\

    <%def name="header()">${c.title}</%def>

    <p>This page doesn't exist yet.
      <a href="${url('edit_page', title=c.title)}">Create the page</a>.
    </p>

At this point we can test our QuickWiki to see how it looks. If you don't already have a server running, start it now with: 

.. code-block :: bash 

    $ paster serve --reload development.ini 

Visit ``http://127.0.0.1:5000/`` and you will see the front page of the wiki. If you haven't already done so, you should delete the file :file:`public/index.html` so that when you visit the URL above you are routed to the correct action in the page controller and see the wiki front page instead of the :file:`index.html` file being displayed. 

We can spruce up the appearance of page a little by adding the stylesheet we linked to in the :file:`templates/base.mako` file earlier. Add the file :file:`public/quick.css` with the following content and refresh the page to reveal a better looking wiki: 

.. code-block :: css 

    body {
      background-color: #888;
      margin: 25px;
    }

    div.content {
      margin: 0;
      margin-bottom: 10px;
      background-color: #d3e0ea;
      border: 5px solid #333;
      padding: 5px 25px 25px 25px;
    }

    h1.main {
      width: 100%;
    }

    p.footer{
      width: 100%;
      padding-top: 8px;
      border-top: 1px solid #000;
    }

    a {
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

When you run the example you will notice that the word ``QuickWiki`` has been turned into a hyperlink by the :func:`get_wiki_content` method we added to our :class:`Page` domain object earlier. You can click the link and will see an example of the new page screen from the :file:`new.mako` template. If you follow the ``Create the page`` link you will see the Pylons automatic error handler kick in to tell you ``Action edit is not implemented``. Well, we better write it next, but before we do, have a play with the :ref:`interactive_debugging`, try clicking on the ``+`` or ``>>`` arrows and you will be able to interactively debug your application. It is a tremendously useful tool.

:meth:`edit` 
------------

To edit the wiki page we need to get the content from the database without changing it to HTML to display it in a simple form for editing. Add the :meth:`edit` action: 

.. code-block :: python 

    def edit(self, title):
        page = self.page_q.filter_by(title=title).first()
        if page:
            c.content = page.content
        return render('/pages/edit.mako')

and then create the ``templates/edit.mako`` file: 

.. code-block :: html+mako  

    <%inherit file="/base.mako"/>\

    <%def name="header()">Editing ${c.title}</%def>

    ${h.secure_form(url('save_page', title=c.title))}
      ${h.textarea(name='content', rows=7, cols=40, content=c.content)} <br />
      ${h.submit(value='Save changes', name='commit')}
    ${h.end_form()}

.. note :: You may have noticed that we only set ``c.content`` if the page exists but that it is accessed in ``h.text_area`` even for pages that don't exist and yet it doesn't raise an ``AttributeError``. 

We are making use of the fact that the ``c`` object returns an empty string ``""`` for any attribute that is accessed which doesn't exist. This can be a very useful feature of the ``c`` object, but can catch you on occasions where you don't expect this behavior. It can be disabled by setting ``config['pylons.strict_c'] = True`` in your project's :file:`config/environment.py`. 

We are making use of the ``h`` object to create our form and field objects. This saves a bit of manual HTML writing. The form submits to the ``save()`` action to save the new or updated content so let's write that next. 

:meth:`save` 
--------------

The first thing the :meth:`save` action has to do is to see if the page being saved already exists. If not it creates it with ``page = model.Page(title)``. Next it needs the updated content. In Pylons you can get request parameters from form submissions via ``GET`` and ``POST`` requests from the appropriately named ``request`` object. For form submissions from *only* ``GET`` or ``POST`` requests, use ``request.GET`` or ``request.POST``. Only ``POST`` requests should generate side effects (like changing data), so the save action will only reference ``request.POST`` for the parameters.

Then add the :meth:`save` action: 

.. code-block :: python 

    @authenticate_form
    def save(self, title):
        page = self.page_q.filter_by(title=title).first()
        if not page:
            page = Page(title)
        # In a real application, you should validate and sanitize
        # submitted data throughly! escape is a minimal example here.
        page.content = escape(request.POST.getone('content'))
        Session.add(page)
        Session.commit()
        flash('Successfully saved %s!' % title)
        redirect_to('show_page', title=title)

.. note :: 
    ``request.POST`` is a MultiDict object: an ordered dictionary that may contain multiple values for each key. The MultiDict will always return one value for any existing key via the normal dict accessors ``request.POST[key]`` and ``request.POST.get(key)``. When multiple values are expected, use the ``request.POST.getall(key)`` method to return all values in a list. ``request.POST.getone(key)`` ensures one value for key was sent, raising a :class:`KeyError` when there are 0 or more than 1 values. 

The :func:`@authenticate_form` decorator that appears immediately before the  :meth:`save` action checks the value of the hidden form field placed there by the :func:`secure_form` helper that we used in :file:`templates/edit.mako` to create the form. The hidden form field carries an authorization token for prevention of certain `Cross-site request forgery (CSRF) <http://en.wikipedia.org/wiki/Cross-site_request_forgery>`_ attacks.

Upon a successful save, we want to redirect back to the :meth:`show` action and 'flash' a ``Successfully saved`` message at the top of the page. 'Flashing' a status message immediately after an action is a common requirement, and the `WebHelpers` package provides the :class:`webhelpers.pylonslib.Flash` class that makes it easy. To utilize it, we'll create a flash object at the bottom of our :file:`lib/helpers.py` module:

.. code-block :: python

    from webhelpers.pylonslib import Flash as _Flash

    flash = _Flash()

And import it into our :file:`controllers/pages.py`. Our new :meth:`show` method
is escaping the content via Python's :func:`cgi.escape` function, so we need to
import that too, and also :func:`@authenticate_form`.

.. code-block :: python 

    from cgi import escape

    from pylons.decorators.secure import authenticate_form

    from quickwiki.lib.helpers import flash

And finally utilize the ``flash`` object in our :file:`templates/base.mako` template:

.. code-block :: html+mako

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html>
      <head>
        <title>QuickWiki</title>
        ${h.stylesheet_link('/quick.css')}
      </head>

      <body>
        <div class="content">
          <h1 class="main">${self.header()}</h1>

          <% flashes = h.flash.pop_messages() %>
          % if flashes:
            % for flash in flashes:
            <div id="flash">
              <span class="message">${flash}</span>
            </div>
            % endfor
          % endif

          ${next.body()}\
          <p class="footer"> 
              Return to the 
              ${h.link_to('FrontPage', 
                  url(action="index", title="FrontPage"))} 
              | ${h.link_to('Edit ' + c.title, 
                  url(title=c.title, action='edit'))} 
          </p> 
        </div>
      </body>
    </html>

And add the following to the :file:`public/quick.css` file: 

.. code-block :: css 

    div#message{ 
        color: orangered; 
    } 

The ``%`` syntax is used for control structures in mako -- conditionals and loops. You must 'close' them with an 'end' tag as shown here. At this point we have a fully functioning wiki that lets you create and edit pages and can be installed and deployed by an end user with just a few simple commands. 

Visit ``http://127.0.0.1:5000`` and have a play. 

It would be nice to get a title list and to be able to delete pages, so that's what we'll do next! 

:meth:`index`
-------------
Add the :meth:`index` action:

.. code-block :: python 

    def index(self):
        c.titles = [page.title for page in self.page_q.all()]
        return render('/pages/index.mako')

The :meth:`index` action simply gets all the pages from the database. Create the :file:`templates/index.mako` file to display the list:

.. code-block:: html+mako

    <%inherit file="/base.mako"/>\

    <%def name="header()">Title List</%def>

    <ul id="titles">
      % for title in c.titles:
      <li>
        ${title} [${h.link_to('visit', url('show_page', title=title))} -
        ${h.link_to('delete', url('delete_page', title=title))}]
      </li>
      % endfor
    </ul>

We need to edit :file:`templates/base.mako` to add a link to the title list in the footer, but while we're at it, let's introduce a Mako function to make the footer a little smarter. Edit :file:`base.mako` like this: 

.. code-block :: html+mako  

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
      "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html>
      <head>
        <title>QuickWiki</title>
        ${h.stylesheet_link('/quick.css')}
      </head>

      <body>
        <div class="content">
          <h1 class="main">${self.header()}</h1>
      
          <% flashes = h.flash.pop_messages() %>
          % if flashes:
            % for flash in flashes:
            <div id="flash">
              <span class="message">${flash}</span>
            </div>
            % endfor
          % endif
      
          ${next.body()}\
      
          <p class="footer">
          ${self.footer(request.environ['pylons.routes_dict']['action'])}\
          </p>
        </div>
      </body>
    </html>

    ## Don't show links that are redundant for particular pages
    <%def name="footer(action)">\
      Return to the ${h.link_to('FrontPage', url('home'))}
      % if action == "index":
        <% return %>
      % endif
      % if action != 'edit':
        | ${h.link_to('Edit ' + c.title, url('edit_page', title=c.title))}
      % endif
      | ${h.link_to('Title List', url('pages'))}
    </%def>

The ``<%def name="footer(action">`` creates a Mako function for display logic. As you can see, the function builds the HTML for the footer, but doesn't display the 'Edit' link when you're on the 'Title List' page or already on an edit page. It also won't show a 'Title List' link when you're already on that page. The ``<% ... %>`` tags shown on the ``return`` statement are the final new piece of Mako syntax: they're used much like the ``${...}`` tags, but for arbitrary Python code that does not directly render HTML. Also, the double hash (``##``) denotes a single-line comment in Mako. 

So the :func:`footer` function is called in place of our old 'static' footer markup. We pass it a value from ``pylons.routes_dict`` which holds the name of the action for the current request. The trailing `\\` character just tells Mako not to render an extra newline. 

If you visit ``http://127.0.0.1:5000/pages`` you should see the full titles list and you should be able to visit each page. 

:meth:`delete` 
----------------

We need to add a :meth:`delete` action that deletes a page, then returns us to the list of titles excluding the one that was deleted: 

.. code-block :: python 

    def delete(self, title):
        page = self.page_q.filter_by(title=title).one()
        Session.delete(page)
        Session.commit()
        flash('Deleted %s.' % title)
        redirect_to('pages')

The title of the page is used to identify and load the object which is then deleted. The change is saved with :func:`model.Session.commit` before the list of remaining titles is re-rendered by the template :file:`templates/index.mako`. 

Visit ``http://127.0.0.1:5000/index`` and have a go at deleting some pages. You may need to go back to the FrontPage and create some more if you get carried away! 

That's it! A working, production-ready wiki in 20 mins. You can visit ``http://127.0.0.1:5000/`` once more to admire your work. 

Publishing the Finished Product 
=============================== 

After all that hard work it would be good to distribute the finished package wouldn't it? Luckily this is really easy in Pylons too. In the project root directory run this command: 

.. code-block :: bash 

    $ python setup.py bdist_egg 

This will create an egg file in ``dist`` which contains everything anyone needs to run your program. They can install it with: 

.. code-block :: bash 

    $ easy_install QuickWiki-0.1.6-py2.5.egg 

You should probably make eggs for each version of Python your users might require by running the above commands with both Python 2.4 and 2.5 to create both versions of the eggs. 

If you want to register your project with PyPi at ``http://www.python.org/pypi`` you can run the command below. *Please only do this with your own projects though because QuickWiki has already been registered!* 

.. code-block :: bash 

    $ python setup.py register 

.. warning:: The PyPi authentication is very weak and passwords are transmitted in plain text. Don't use any sign in details that you use for important applications as they could be easily intercepted. 

You will be asked a number of questions and then the information you entered in ``setup.py`` will be used as a basis for the page that is created. 

Now visit ``http://www.python.org/pypi`` to see the new index with your new package listed. 

.. note :: A `CheeseShop Tutorial <http://wiki.python.org/moin/CheeseShopTutorial>`_ has been written and `full documentation on setup.py <http://docs.python.org/dist/dist.html>`_ is available from the Python website. You can even use `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ in the ``description`` and ``long_description`` areas of ``setup.py`` to add formatting to the pages produced on PyPi (PyPi used to be called "the CheeseShop"). There is also `another tutorial here <http://www.python.org/~jeremy/weblog/030924.html>`_. 

Finally you can sign in to PyPi with the account details you used when you registered your application and upload the eggs you've created. If that seems too difficult you can even use this command which should be run for each version of Python supported to upload the eggs for you: 

.. code-block :: bash 

    $ python setup.py bdist_egg upload 

Before this will work you will need to create a :file:`.pypirc` file in your home directory containing your username and password so that the ``upload`` command knows who to sign in as. It should look similar to this: 

.. code-block :: ini

    [server-login] 
    username: james 
    password: password 

.. note :: This works on windows too but you will need to set your ``HOME`` environment variable first. If your home directory is ``C:\Documents and Settings\James`` you would put your :file:`.pypirc` file in that directory and set your ``HOME`` environment variable with this command: 

.. code-block :: bash 

    > SET HOME=C:\Documents and Settings\James 

You can now use the ``python setup.py bdist_egg upload`` as normal. 

Now that the application is on PyPi anyone can install it with the ``easy_install`` command exactly as we did right at the very start of this tutorial. 

Security 
======== 

A final word about security. 

.. warning :: Always set ``debug = false`` in configuration files for production sites and make sure your users do too. 

You should NEVER run a production site accessible to the public with debug mode on. If there was a problem with your application and an interactive error page was shown, the visitor would be able to run any Python commands they liked in the same way you can when you are debugging. This would obviously allow them to do all sorts of malicious things so it is very important you turn off interactive debugging for production sites by setting ``debug = false`` in configuration files and also that you make users of your software do the same. 

Summary 
======= 

We've gone through the whole cycle of creating and distributing a Pylons application looking at setup and configuration, routing, models, controllers and templates. Hopefully you have an idea of how powerful Pylons is and, once you get used to the concepts introduced in this tutorial, how easy it is to create sophisticated, distributable applications with Pylons. 

That's it, I hope you found the tutorial useful. You are encouraged to email any comments to the `Pylons mailing list <http://groups.google.com/group/pylons-discuss>`_ where they will be welcomed. 

ToDo 
==== 

* If QuickWiki is intended as a reference app for Pylons best practices, I'd like to incorporate some testing into the tutorial. Possibly introduce ``paster shell`` too. 

Thanks 
====== 
A big thanks to Ches Martin for updating this document and the QuickWiki project for Pylons 0.9.6 / Pylons 0.9.7 / QuickWiki 0.1.5 / QuickWiki 0.1.6, Graham Higgins, and others in the Pylons community who contributed bug fixes and suggestions. 

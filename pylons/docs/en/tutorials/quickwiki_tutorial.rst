.. _quickwiki_tutorial:

==================
Quickwiki tutorial
==================

Introduction 
============ 

If you haven't done so already, please first read the :ref:`getting_started` guide. 

In this tutorial we are going to create a working wiki from scratch using Pylons 1.0 and `SQLAlchemy`_. Our wiki will allow visitors to add, edit or delete formatted wiki pages. 

Starting at the End 
=================== 

Pylons is designed to be easy for everyone, not just developers, so let's start by downloading and installing the finished QuickWiki in exactly the same way that end users of QuickWiki might do. Once we have explored its features we will set about writing it from scratch.

After you have :ref:`installed Pylons <installing_pylons>`, install the QuickWiki project: 

.. code-block :: bash 

    $ easy_install QuickWiki==0.1.8
    $ paster make-config QuickWiki test.ini 

Next, ensure that the ``sqlalchemy.url`` variable in the ``[app:main]`` section of the configuration file (``development.ini``) specifies a value that is suitable for your setup. The data source name points to the database you wish to use.

.. note :: 

    The default ``sqlite:///%(here)s/quickwiki.db`` uses a (file-based) SQLite database named ``quickwiki.db`` in the ini's top-level directory. This SQLite database will be created for you when running the :command:`paster setup-app` command below, but you could also use MySQL, Oracle or PostgreSQL. Firebird and MS-SQL may also work. See the `SQLAlchemy documentation <http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments>`_ for more information on how to connect to different databases. SQLite for example requires additional forward slashes in its URI, where the client/server databases should only use two. You will also need to make sure you have the appropriate Python driver for the database you wish to use. If you're using Python 2.5, a version of the `pysqlite adapter <http://www.initd.org/tracker/pysqlite/wiki/pysqlite>`_ is already included, so you can jump right in with the tutorial. You may need to get `SQLite itself <http://www.sqlite.org/download.html>`_. 

Finally create the database tables and serve the finished application: 

.. code-block :: bash 

    $ paster setup-app test.ini 
    $ paster serve test.ini 

That's it! Now you can visit http://127.0.0.1:5000 and experiment with the finished Wiki. 

When you've finished, stop the server with :kbd:`Control-C` so we can start developing our own version. 

If you are interested in looking at the latest version of the QuickWiki source code it can be browsed online at http://bitbucket.org/bbangert/quickwiki/src/ or can be checked out using `Mercurial <http://www.selenic.com/mercurial/>`_:

.. code-block :: bash 

    $ hg clone http://bitbucket.org/bbangert/quickwiki 

.. Note::

    To run the QuickWiki checked out from the repository, you'll need to first run :command:`python setup.py develop` from the project's root directory. This will install its dependencies and generate `Python Egg <http://peak.telecommunity.com/DevCenter/PythonEggs>`_ metadata in a :file:`QuickWiki.egg-info` directory. The latter is required for the :command:`paster` command (among other things) .

    .. code-block :: bash 

        $ cd QuickWiki
        $ python setup.py develop

Developing QuickWiki 
==================== 

If you skipped the "Starting at the End" section you will need to assure yourself that you have Pylons installed. See the :ref:`getting_started`.

Then create your project: 

.. code-block :: bash 

    $ paster create -t pylons QuickWiki

When prompted for which templating engine to use, simply hit enter for the default (Mako). When prompted for SQLAlchemy configuration, enter ``True``.

Now let's start the server and see what we have: 

.. code-block :: bash 

    $ cd QuickWiki 
    $ paster serve --reload development.ini 

.. note :: We have started :command:`paster serve` with the :option:`--reload` option. This means any changes that we make to code will cause the server to restart (if necessary); your changes are immediately reflected on the live site. 

Visit http://127.0.0.1:5000 where you will see the introduction page. Now delete the file :file:`public/index.html` so we can see the front page of the wiki instead of this welcome page. If you now refresh the page, the Pylons built-in error document support will kick in and display an ``Error 404`` page, indicating the file could not be found. We'll setup a controller to handle this location later.


The Model 
========= 

Pylons uses a Model-View-Controller architecture; we'll start by creating the model. We could use any system we like for the model, including `SQLAlchemy`_ or `SQLObject <http://www.sqlobject.org>`_. Optional SQLAlchemy integration is provided for new Pylons projects, which we enabled when creating the project, and thus we'll be using SQLAlchemy for the QuickWiki. 

.. note :: `SQLAlchemy`_ is a powerful Python SQL toolkit and Object Relational Mapper (ORM) that is widely used by the Python community. 

SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performance database access, adapted into a simple and Pythonic domain language. It has full and detailed documentation available on the SQLAlchemy website: http://sqlalchemy.org/docs/.

The most basic way of using SQLAlchemy is with explicit sessions where you create :class:`Session` objects as needed.

Pylons applications typically employ a slightly more sophisticated setup, using SQLAlchemy's "contextual" thread-local sessions created via the :meth:`sqlalchemy.orm.scoped_session` function. With this configuration, the application can use a single :class:`Session` instance per web request, avoiding the need to pass it around explicitly. Instantiating a new scoped :class:`Session` will actually find an existing one in the current thread if available. Pylons has setup a :class:`Session` for us in the :file:`model/meta.py` file. For further details, refer to the `SQLAlchemy documentation on the Session <http://www.sqlalchemy.org/docs/05/session.html#contextual-thread-local-sessions>`_.

.. note :: It is important to recognize the difference between SQLAlchemy's (or possibly another DB abstraction layer's) :class:`Session` object and Pylons' standard :dfn:`session` (with a lowercase 's') for web requests. See :mod:`beaker` for more on the latter. It is customary to reference the database session by :class:`model.Session` or (more recently) :class:`Session` outside of model classes.

The :file:`model/__init__.py` file starts out rather bare-bones. It initializes the SQLAlchemy database engine, and imports the Session object.

At the top, add the following imports::
    
    from sqlalchemy import orm, Column, Unicode, UnicodeText
    from quickwiki.model.meta import Session, Base

Then add the following to the end of the :file:`model/__init__.py` file: 

.. code-block :: python 
    
    class Page(Base):
        __tablename__ = 'pages'
        title = Column(Unicode(40), primary_key=True)
        content = Column(UnicodeText(), default=u'')

We've defined a table called ``pages`` which has two columns: ``title`` (the primary key), a Unicode VARCHAR of 40 characters, and ``content`` a Unicode TEXT column of variable sized length. 

.. note :: A primary key is a unique ID for each row in a database table. In the example above we are using the page title as a natural primary key. Some prefer to integer primary keys for all tables, so-called surrogate primary keys. The author of this tutorial uses both methods in his own code and is not advocating one method over the other, what's important is to choose the best database structure for your application. See the Pylons Cookbook for `a quick general overview of relational databases <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_ if you're not familiar with these concepts. 

A core philosophy of ORMs is that tables and domain classes are different beasts. So next we'll create the Python class that represents the pages of our wiki, and map these domain objects to rows in the ``pages`` table via the :func:`sqlalchemy.orm.mapper` function. In a more complex application, you could break out model classes into separate ``.py`` files in your :file:`model` directory, but for sake of simplicity in this case, we'll just stick to :file:`__init__.py`. 

Add this to the bottom of ``model/__init__.py``: 

.. code-block :: python 

    class Page(object): 

        def __init__(self, title, content=None):
            self.title = title
            self.content = content

        def __unicode__(self):
            return self.title

        __str__ = __unicode__

    orm.mapper(Page, pages_table) 

A :class:`Page` object represents a row in the ``pages`` table, so ``self.title`` and ``self.content`` will be the values of the ``title`` and ``content`` columns.

Looking ahead, our wiki could use a way of marking up the ``content`` field into HTML. Also, any 'WikiWords' (words made by joining together two or more capitalized words) should be converted to hyperlinks to wiki pages.

We can use Python's `docutils <http://docutils.sourceforge.net/>`_ library to allow marking up ``content`` as `reStructuredText`_. So next we'll add a method to our :class:`Page` class that formats ``content`` as HTML and converts the WikiWords to hyperlinks. Add the following at the top of the :file:`model/__init__.py` file: 

.. code-block :: python 

    import logging
    import re
    import sets
    from docutils.core import publish_parts

    from pylons import url
    from quickwiki.lib.helpers import link_to
    from quickwiki.model import meta

    log = logging.getLogger(__name__)

    # disable docutils security hazards:
    # http://docutils.sourceforge.net/docs/howto/security.html
    SAFE_DOCUTILS = dict(file_insertion_enabled=False, raw_enabled=False)
    wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE)

then add a :meth:`get_wiki_content` method to the :class:`Page` class:

.. code-block :: python 

    class Page(object):

        def __init__(self, title, content=None):
            self.title = title
            self.content = content

        def get_wiki_content(self):
            """Convert reStructuredText content to HTML for display, and
            create links for WikiWords
            """
            content = publish_parts(self.content, writer_name='html',
                                    settings_overrides=SAFE_DOCUTILS)['html_body']
            titles = sets.Set(wikiwords.findall(content))
            for title in titles:
                title_url = url(controller='pages', action='show', title=title)
                content = content.replace(title, link_to(title, title_url))
            return content

        def __unicode__(self):
            return self.title

        __str__ = __unicode__

The :class:`Set` object provides us with only unique WikiWord names, so we don't try replacing them more than once (a "wikiword" is of course defined by the regular expression set globally).

.. note :: 

    Pylons uses a **Model View Controller** architecture and so the formatting of objects into HTML should properly be handled in the View, i.e. in a template. However in this example, converting `reStructuredText`_ into HTML in a template is inappropriate so we are treating the HTML representation of the content as part of the model. It also gives us the chance to demonstrate that SQLAlchemy domain classes are real Python classes that can have their own methods. 

The :func:`link_to` and :func:`url` functions referenced in the controller code are respectively: a helper imported from the :mod:`webhelpers.html` module indirectly via :file:`lib/helpers.py`, and a utility function imported directly from the :mod:`pylons` module. They are utilities for creating links to specific controller actions. In this case we have decided that all WikiWords should link to the :meth:`show` action of the ``pages`` controller which we'll create later. However, we need to ensure that the :func:`link_to` function is made available as a helper by adding an import statement to :file:`lib/helpers.py`:

.. code-block :: python

    """Helper functions

    Consists of functions to typically be used within templates, but also
    available to Controllers. This module is available to templates as 'h'.
    """
    from webhelpers.html.tags import *

Since we have used docutils and SQLAlchemy, both third party packages, we need to edit our :file:`setup.py` file so that anyone installing QuickWiki with `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ will automatically have these dependencies installed too. Edit your :file:`setup.py` in your project root directory and add a docutils entry to the ``install_requires`` line (there will already be one for SQLAlchemy): 

.. code-block :: python 

    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "docutils==0.4",
    ],

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

    The command :command:`python setup.py develop` installs your application in a special mode so that it behaves exactly as if it had been installed as an egg file by an end user. This is really useful when you are developing an application because it saves you having to create an egg and install it every time you want to test a change. 

Application Setup 
=================

Edit :file:`websetup.py`, used by the :command:`paster setup-app` command, to look like this: 

.. code-block :: python 

    """Setup the QuickWiki application"""
    import logging

    from quickwiki import model
    from quickwiki.config.environment import load_environment
    from quickwiki.model import meta
    
    log = logging.getLogger(__name__)

    def setup_app(command, conf, vars):
        """Place any commands to setup quickwiki here"""
        load_environment(conf.global_conf, conf.local_conf)

        # Create the tables if they don't already exist
        log.info("Creating tables...")
        meta.metadata.create_all(bind=meta.engine)
        log.info("Successfully set up.")

        log.info("Adding front page data...")
        page = model.Page(title=u'FrontPage',
                          content=u'**Welcome** to the QuickWiki front page!')
        meta.Session.add(page)
        meta.Session.commit()
        log.info("Successfully set up.")


You can see that :file:`config/environment.py`'s :func:`load_environment` function is called (which calls :file:`model/__init__.py`'s :func:`init_model` function), so our engine is ready for binding and we can import the model. A SQLAlchemy :class:`MetaData` object -- which provides some utility methods for operating on database schema -- usually needs to be connected to an engine, so the line  

.. code-block :: python

    meta.metadata.bind = meta.engine

does exactly that and then

.. code-block :: python

    model.metadata.create_all(checkfirst=True)

uses the connection we've just set up and, creates the table(s) we've defined ... if they don't already exist. After the tables are created, the other lines add some data for the simple front page to our wiki.

By default, SQLAlchemy specifies ``autocommit=False`` when creating the :class:`Session`, which means that operations will be wrapped in a transaction and :func:`commit`'ed atomically (unless your DB doesn't support transactions, like MySQL's default MyISAM tables -- but that's beyond the scope of this tutorial). 

The database SQLAlchemy will use is specified in the ``ini`` file, under the ``[app:main]`` section, as ``sqlalchemy.url``. We'll customize the ``sqlalchemy.url`` value to point to a SQLite database named :file:`quickwiki.db` that will reside in your project's root directory. Edit the :file:`development.ini` file in the root directory of your project:

.. note :: 

    If you've decided to use a different database other than SQLite, see the SQLAlchemy note in the `Starting at the End`_ section for information on supported database URIs.

.. code-block :: ini

    [app:main] 
    use = egg:QuickWiki 
    #... 
    # Specify the database for SQLAlchemy to use. 
    # SQLAlchemy database URL
    sqlalchemy.url = sqlite:///%(here)s/quickwiki.db 

You can now run the :command:`paster setup-app` command to setup your tables in the same way an end user would, remembering to drop and recreate the database if the version tested earlier has already created the tables: 

.. code-block :: bash 

    $ paster setup-app development.ini

You should see the SQL sent to the database as the default :file:`development.ini` is setup to log SQLAlchemy's SQL statements.

At this stage you will need to ensure you have the appropriate Python database drivers for the database you chose, otherwise you might find SQLAlchemy complains it can't get the DBAPI module for the dialect it needs. 

You should also edit :file:`quickwiki/config/deployment.ini_tmpl` so that when users run :command:`paster make-config` the configuration file that is produced for them will also use :file:`quickwiki.db`. In the ``[app:main]`` section: 

.. code-block :: ini 

    # Specify the database for SQLAlchemy to use. 
    sqlalchemy.url = sqlite:///%(here)s/quickwiki.db 

Templates 
========= 

.. note :: 

    Pylons uses the `Mako templating engine <http://www.makotemplates.org>`_ by default, although as is the case with most aspects of Pylons, you are free to deviate from the default if you prefer.

In our project we will make use of the `Mako inheritance feature <http://www.makotemplates.org/docs/inheritance.html>`_. Add the main page template in :file:`templates/base.mako`: 

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
            Return to the ${h.link_to('FrontPage', url('FrontPage'))}
            | ${h.link_to('Edit ' + c.title, url('edit_page', title=c.title))}
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
    map.connect('delete_page', '/pages/delete', controller='pages',
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

and then create the :file:`templates/edit.mako` file: 

.. code-block :: html+mako  

    <%inherit file="/base.mako"/>\

    <%def name="header()">Editing ${c.title}</%def>

    ${h.secure_form(url('save_page', title=c.title))}
      ${h.textarea(name='content', rows=7, cols=40, content=c.content)} <br />
      ${h.submit(value='Save changes', name='commit')}
    ${h.end_form()}

.. note :: You may have noticed that we only set ``c.content`` if the page exists but that it is accessed in :func:`h.text_area` even for pages that don't exist and yet it doesn't raise an :class:`AttributeError`. 

We are making use of the fact that the ``c`` object returns an empty string ``""`` for any attribute that is accessed which doesn't exist. This can be a very useful feature of the ``c`` object, but can catch you on occasions where you don't expect this behavior. It can be disabled by setting ``config['pylons.strict_c'] = True`` in your project's :file:`config/environment.py`. 

We are making use of the ``h`` object to create our form and field objects. This saves a bit of manual HTML writing. The form submits to the :meth:`save()` action to save the new or updated content so let's write that next. 

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
    ``request.POST`` is a MultiDict object: an ordered dictionary that may contain multiple values for each key. The MultiDict will always return one value for any existing key via the normal dict accessors ``request.POST[key]`` and :meth:`request.POST.get`. When multiple values are expected, use the :meth:`request.POST.getall` method to return all values in a list. :meth:`request.POST.getone` ensures one value for key was sent, raising a :class:`KeyError` when there are 0 or more than 1 values. 

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
            Return to the ${h.link_to('FrontPage', url('FrontPage'))}
            | ${h.link_to('Edit ' + c.title, url('edit_page', title=c.title))}
          </p> 
        </div>
      </body>
    </html>

And add the following to the :file:`public/quick.css` file: 

.. code-block :: css 

    div#flash .message {
      color: orangered;
    }

The ``%`` syntax is used for control structures in mako -- conditionals and loops. You must 'close' them with an 'end' tag as shown here. At this point we have a fully functioning wiki that lets you create and edit pages and can be installed and deployed by an end user with just a few simple commands. 

Visit http://127.0.0.1:5000 and have a play. 

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

    ${h.secure_form(url('delete_page'))}

    <ul id="titles">
      % for title in c.titles:
      <li>
        ${h.link_to(title, url('show_page', title=title))} -
        ${h.checkbox('title', title)}
      </li>
      % endfor
    </ul>

    ${h.submit('delete', 'Delete')}

    ${h.end_form()}

This displays a form listing a link to all pages along with a checkbox. When submitted, the selected titles will be sent to a :meth:`delete` action we'll create in the next step.

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

The ``<%def name="footer(action">`` creates a Mako function for display logic. As you can see, the function builds the HTML for the footer, but doesn't display the 'Edit' link when you're on the 'Title List' page or already on an edit page. It also won't show a 'Title List' link when you're already on that page. The ``<% ... %>`` tags shown on the :keyword:`return` statement are the final new piece of Mako syntax: they're used much like the ``${...}`` tags, but for arbitrary Python code that does not directly render HTML. Also, the double hash (``##``) denotes a single-line comment in Mako. 

So the :func:`footer` function is called in place of our old 'static' footer markup. We pass it a value from ``pylons.routes_dict`` which holds the name of the action for the current request. The trailing `\\` character just tells Mako not to render an extra newline. 

If you visit http://127.0.0.1:5000/pages you should see the full titles list and you should be able to visit each page. 

:meth:`delete` 
----------------

We need to add a :meth:`delete` action that deletes pages submitted from :file:`templates/index.mako`, then returns us back to the list of titles (excluding those that were deleted): 

.. code-block :: python 

    @authenticate_form
    def delete(self):
        titles = request.POST.getall('title')
        pages = self.page_q.filter(Page.title.in_(titles))
        for page in pages:
            Session.delete(page)
        Session.commit()
        # flash only after a successful commit
        for title in titles:
            flash('Deleted %s.' % title)
        redirect_to('pages')

Again we use the :func:`@authenticate_form` decorator along with :func:`secure_form` used in :file:`templates/index.mako`. We're expecting potentially multiple titles, so we use :meth:`request.POST.getall` to return a list of titles. The titles are used to identify and load the :class:`Page` objects, which are then deleted.

We use the SQL ``IN`` operator to match multiple titles in one query. We can do this via the more flexible :meth:`filter` method which can accept an :meth:`in_` clause created via the title column's attribute.

The :meth:`filter_by` method we used in previous methods is a shortcut for the most typical filtering clauses. For example, the :meth:`show` method's:

.. code-block :: python 

    self.page_q.filter_by(title=title)

is equivalent to:

.. code-block :: python 

    self.page_q.filter(Page.title == title)

After deleting the pages, the changes are committed, and only after successfully committing do we flash deletion messages. That way if there was a problem with the commit no flash messages are shown. Finally we redirect back to the index page, which re-renders the list of remaining titles.

Visit http://127.0.0.1:5000/index and have a go at deleting some pages. You may need to go back to the FrontPage and create some more if you get carried away! 

That's it! A working, production-ready wiki in 20 mins. You can visit http://127.0.0.1:5000/ once more to admire your work. 

Publishing the Finished Product 
=============================== 

After all that hard work it would be good to distribute the finished package wouldn't it? Luckily this is really easy in Pylons too. In the project root directory run this command: 

.. code-block :: bash 

    $ python setup.py bdist_egg 

This will create an egg file in the :file:`dist` directory which contains everything anyone needs to run your program. They can install it with: 

.. code-block :: bash 

    $ easy_install QuickWiki-0.1.6-py2.5.egg 

You should probably make eggs for each version of Python your users might require by running the above commands with both Python 2.4 and 2.5 to create both versions of the eggs. 

If you want to register your project with PyPi at http://www.python.org/pypi you can run the command below. *Please only do this with your own projects though because QuickWiki has already been registered!* 

.. code-block :: bash 

    $ python setup.py register 

.. warning:: The PyPi authentication is very weak and passwords are transmitted in plain text. Don't use any sign in details that you use for important applications as they could be easily intercepted. 

You will be asked a number of questions and then the information you entered in :file:`setup.py` will be used as a basis for the page that is created. 

Now visit http://www.python.org/pypi to see the new index with your new package listed. 

.. note :: A `CheeseShop Tutorial <http://wiki.python.org/moin/CheeseShopTutorial>`_ has been written and `full documentation on setup.py <http://docs.python.org/dist/dist.html>`_ is available from the Python website. You can even use `reStructuredText`_ in the ``description`` and ``long_description`` areas of :file:`setup.py` to add formatting to the pages produced on PyPi (PyPi used to be called "the CheeseShop"). There is also `another tutorial here <http://www.python.org/~jeremy/weblog/030924.html>`_. 

Finally you can sign in to PyPi with the account details you used when you registered your application and upload the eggs you've created. If that seems too difficult you can even use this command which should be run for each version of Python supported to upload the eggs for you: 

.. code-block :: bash 

    $ python setup.py bdist_egg upload 

Before this will work you will need to create a :file:`.pypirc` file in your home directory containing your username and password so that the :command:`upload` command knows who to sign in as. It should look similar to this: 

.. code-block :: ini

    [server-login] 
    username: james 
    password: password 

.. note :: This works on windows too but you will need to set your :envvar:`HOME` environment variable first. If your home directory is :file:`C:\Documents and Settings\James` you would put your :file:`.pypirc` file in that directory and set your :envvar:`HOME` environment variable with this command: 

.. code-block :: bash 

    > SET HOME=C:\Documents and Settings\James 

You can now use the :command:`python setup.py bdist_egg upload` as normal. 

Now that the application is on PyPi anyone can install it with the :command:`easy_install` command exactly as we did right at the very start of this tutorial. 

Security 
======== 

A final word about security. 

.. warning :: Always set ``debug = false`` in configuration files for production sites and make sure your users do too. 

You should NEVER run a production site accessible to the public with debug mode on. If there was a problem with your application and an interactive error page was shown, the visitor would be able to run any Python commands they liked in the same way you can when you are debugging. This would obviously allow them to do all sorts of malicious things so it is very important you turn off interactive debugging for production sites by setting ``debug = false`` in configuration files and also that you make users of your software do the same. 

Summary 
======= 

We've gone through the whole cycle of creating and distributing a Pylons application looking at setup and configuration, routing, models, controllers and templates. Hopefully you have an idea of how powerful Pylons is and, once you get used to the concepts introduced in this tutorial, how easy it is to create sophisticated, distributable applications with Pylons. 

That's it, I hope you found the tutorial useful. You are encouraged to email any comments to the `Pylons mailing list <http://groups.google.com/group/pylons-discuss>`_ where they will be welcomed. 

Thanks 
====== 
A big thanks to Ches Martin for updating this document and the QuickWiki project for Pylons 0.9.6 / Pylons 0.9.7 / QuickWiki 0.1.5 / QuickWiki 0.1.6, Graham Higgins, and others in the Pylons community who contributed bug fixes and suggestions. 

Todo 
==== 

* Provide :command:`paster shell` examples
* Incorporate testing into the tutorial
* Explain Ches's :meth:`validate_title` method in the actual QuickWiki project
* Provide snapshots of every file modified at each step, to help resolve mistakes

.. _`SQLAlchemy`: http://www.sqlalchemy.org
.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html

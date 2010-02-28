.. _quickwiki_tutorial:

==================
Quickwiki tutorial
==================

Introduction 
============ 

If you haven't done so already read the :ref:`getting_started` guide. 

In this tutorial we are going to create a working wiki from scratch using Pylons 0.9.6 and SQLAlchemy. Our wiki will allow visitors to add, edit or delete formatted wiki pages. 

Starting at the End 
=================== 

Pylons is designed to be easy for everyone, not just developers, so lets start by downloading and installing the finished QuickWiki in exactly the way end users of QuickWiki might do. Once we have explored its features we will set about writing it from scratch. 

After you have installed `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ run these commands to install QuickWiki and create a config file: 

.. code-block:: bash 

    $ easy_install QuickWiki==0.1.5 
    $ paster make-config QuickWiki test.ini 

Next edit the configuration file by specifying the ``sqlalchemy.default.url`` variable in ``[app:main]`` section so that the data source name points to the database you wish to use. 

.. Note:: 

    The default ``sqlite:///%(here)s/quickwiki.db`` uses a (file-based) SQLite database named ``quickwiki.db`` in the project's top-level directory. This database will be created for you when running the ``paster setup-app`` command below, but you could also use MySQL, Oracle or PostgreSQL. Firebird and MS-SQL may also work. See the `SQLAlchemy documentation <http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_establishing>`_ for more information on how to connect to different databases. SQLite for example requires additional forward slashes in its URI, where the client/server databases should only use two. You will also need to make sure you have the appropriate Python driver for the database you wish to use. If you're using Python 2.5, a version of the `pysqlite adapter <http://www.initd.org/tracker/pysqlite/wiki/pysqlite>`_ is already included, so you can jump right in with the tutorial. You may need to get `SQLite itself <http://www.sqlite.org/download.html>`_. 

Finally create the database tables and serve the finished application: 

.. code-block:: bash 

    $ paster setup-app test.ini 
    $ paster serve test.ini 

That's it! Now you can visit http://127.0.0.1:5000 and experiment with the finished Wiki. Note that in the title list screen you can drag page titles to the trash area to delete them via AJAX calls. 

When you've finished, stop the server with ``CTRL+C`` because we will start developing our own version. 

If you are interested in looking at the latest version of the QuickWiki source code it can be browsed online at http://bitbucket.org/bbangert/quickwiki/src/ or can be checked out using Mercurial: 

.. code-block:: bash 

    $ hg clone http://bitbucket.org/bbangert/quickwiki 

.. Note:: 

    To run the version checked out from the repository, you'll want to run ``python setup.py egg_info`` from the project's root directory. This will generate some files in the ``QuickWiki.egg-info`` directory. 

Note that there is also currently a small bug where running the command doesn't generate a ``paster_plugins.txt`` file in the ``egg-info`` directory. Without this, ``paster shell`` will not work. Create it yourself, and add the text ``Pylons``, ``WebHelpers`` and ``PasteScript`` on separate lines. Hopefully this issue will be fixed soon. 

Developing QuickWiki 
==================== 

If you skipped the "Starting at the End" section you will need to assure that you have Pylons installed. See the :ref:`getting_started`.

Then create your project: 

.. code-block:: bash 

    $ paster create -t pylons QuickWiki 

Now lets start the server and see what we have: 

.. code-block:: bash 

    $ cd QuickWiki 
    $ paster serve --reload development.ini 

.. Note:: We have started the server with the ``--reload`` switch. This means any changes we make to code will cause the server to restart (if necessary); your changes are immediately reflected on the live site. 

Open a new console and ``cd QuickWiki/quickwiki``. Visit http://127.0.0.1:5000 where you will see the introduction page. Delete the file ``public/index.html`` because we want to see the front page of the wiki instead of this welcome page. If you now refresh the page, the Pylons built-in error document support will kick in and display an ``Error 404`` page to tell you the file could not be found. We'll setup a controller to handle this location later. 

The Model 
========= 

Pylons uses a Model View Controller architecture; we'll start by creating the model. We could use any system we like for the model including `SQLObject <http://www.sqlobject.org>`_ or `SQLAlchemy <http://www.sqlalchemy.org>`_. SQLAlchemy is the default for current versions of Pylons, and we'll use it for QuickWiki. 

.. Note:: SQLAlchemy is a Python SQL toolkit and Object Relational Mapper that is fast becoming the default choice for many Python programmers. 

SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performance database access, adapted into a simple and Pythonic domain language. There is full and detailed documentation available on the SQLAlchemy website at http://sqlalchemy.org/docs/ and you should really read this before you get heavily into SQLAlchemy. 

The most basic way of using SQLAlchemy is with explicit sessions where you create ``Session`` objects as needed. Pylons applications typically employ a slightly more sophisticated setup using SQLAlchemy 0.4's "contextual," thread-local sessions, via ``scoped_session``. With this configuration, the application can use a single ``Session`` instance per web request, without the need to pass it around explicitly. Instantiating a new ``Session`` will actually find an existing one in the current thread if available. There are further details in the `SQLAlchemy documentation on the Session <http://www.sqlalchemy.org/docs/04/session.html#unitofwork_contextual>`_. 

.. Note:: 
    It is important to recognize the difference between SQLAlchemy's (or possibly another DB abstraction layer's) ``Session`` object and Pylons' standard ``session`` (with a lowercase 's') for web requests. See :mod:`beaker` for more on the latter. It is customary to reference the database session by ``model.Session`` outside of model classes. 


Now add the following to the end of the contents of your ``model/__init__.py`` file: 

.. code-block:: python 

    from sqlalchemy import Column, MetaData, Table, types 
    pages_table = Table('pages', meta.metadata, 
                    sa.Column('title', sa.types.Unicode(40), primary_key=True), 
                    sa.Column('content', sa.types.Unicode(), default='') 
                    )
    
    class Page(object):
        pass

    orm.mapper(Page, pages_table)

The first line imports Pylons' ``config`` object so we can bind our database ``Session`` to an engine -- more on that in a bit. The second line imports some useful SQLAlchemy objects such as the ``Table`` and ``Column`` classes. The third imports the mapper function which we use to map our table schemas to objects. The final import statement provides two functions for setting up the session and adding the contextual functionality. 

After the imports we setup our ``metadata`` object which is used when defining and managing tables. We then define a table called ``pages`` which has two columns, ``title`` (the primary key) and ``content``. 

.. Note:: 
    SQLAlchemy also supports reflecting table information directly from a database. If we had already created the ``pages`` database table, SQLAlchemy could have constructed the ``pages_table`` object for us. This uses the ``autoload=True`` parameter in place of the ``Column`` definitions, like this: 

.. code-block:: python 

    pages_table = Table('pages', metadata, autoload=True) 

`SQLAlchemy table reflection docs <http://www.sqlalchemy.org/docs/04/metadata.html#metadata_tables_reflecting>`_ 

.. Note:: A primary key is a unique ID for each row in a database table. In the example above we are using the page title as a natural primary key. Some people prefer to use integer primary keys for all tables, so-called surrogate primary keys. The author of this tutorial uses both methods in his own code and is not advocating one method over the other, it is important that you choose the best database structure for your application. See the Pylons Cookbook for `a quick general overview of relational databases <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_ if you're not familiar with these concepts. 

A core philosophy of SQLAlchemy is that tables and domain classes are different beasts. So next, we'll create the Python class that will represent the pages of our wiki and map these domain objects to rows in the ``pages`` table using a mapper. In a more complex application, you could break out model classes into separate ``.py`` files in your ``model`` directory, but for sake of simplicity in this case, we'll just stick to ``__init__.py``. 

Add this to the bottom of ``model/__init__.py``: 

.. code-block:: python 

    class Page(object): 
        def __str__(self): 
            return self.title 

    mapper(Page, pages_table) 

For those familiar with SQLAlchemy 0.3, ``scoped_session`` replaces the ``sessioncontext`` extension, and ``Session.mapper`` could then be used here in place of ``mapper`` to get behavior similar to what used to be achieved with ``assign_mapper``. This is considered an advanced topic, and you should consult SQLAlchemy's documentation if you wish to learn how it works. 

Looking ahead, our wiki will need some formatting so we will need to turn the ``content`` field into HTML. Any WikiWords (which are words made by joining together two or more lowercase words with the first letter capitalized) will also need to be converted into hyperlinks. 

It would be nice if we could add a method to our ``Page`` object to retrieve the formatted HTML with the WikiWords already converted to hyperlinks. Add the following at the top of the ``model/__init__.py`` file: 

.. code-block:: python 

    import re 
    import sets 

    from docutils.core import publish_parts 

    import quickwiki.lib.helpers as h 

    wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)", re.UNICODE) 

and then add a ``get_wiki_content()`` method to the ``Page`` object so it looks like this: 

.. code-block:: python 

    class Page(object): 
        content = None 

        def __str__(self): 
            return self.title 

        def get_wiki_content(self): 
            content = publish_parts(
                self.content, writer_name="html")["html_body"] 
            titles = sets.Set(wikiwords.findall(content)) 
            for title in titles: 
                title_url = h.url_for(controller='page', 
                                      action='index', title=title) 
            content = content.replace(title, h.link_to(title, title_url)) 
            return content 

This code deserves a bit of explaining. The ``content = None`` line is so that the ``content`` attribute is initialized to ``None`` when a new ``Page`` object is created. The ``Page`` object represents a row in the ``pages`` table so ``self.content`` will be the value of the ``content`` field. The ``Set`` object provides us with only unique WikiWord names, so we don't try replacing them more than once (a "wikiword" is of course defined by the regular expression set globally). ``h.link_to()`` and ``h.url_for()`` are standard Pylons helpers which create links to specific controller actions. In this case we have decided that all WikiWords should link to the ``index`` action of the ``page`` controller which we will create later. 

.. Note:: 

    Pylons uses a Model View Controller architecture and so the formatting of objects into HTML should usually be handled in the view, i.e. in a template. In this example converting reStructuredText into HTML in a template is not appropriate so we are treating the HTML representation of the content as part of the model. It also gives us the chance to demonstrate that SQLAlchemy domain classes are real Python classes that can have their own methods. 

One final change, since we have used docutils and SQLAlchemy, both third party packages, we need to edit our ``setup.py`` file so that anyone installing QuickWiki with `Easy Install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ will automatically also have these dependencies installed for them too. Edit your ``setup.py`` in your project root directory so that the ``install_requires`` line looks like this: 

.. code-block:: python 

    install_requires=["Pylons>=0.9.6", "docutils==0.4", "SQLAlchemy>=0.4.1"], 

While we are we are making changes to ``setup.py`` we might want to complete some of the other sections too. Set the version number to 0.1.5 and add a description and URL which will be used on the Python Cheeseshop when we release it: 

.. code-block:: python 

    version="0.1.5", 
    description="QuickWiki - Pylons 0.9.6 Tutorial application", 
    url="http://wiki.pylonshq.com/display/pylonsdocs/QuickWiki+Tutorial", 

We might also want to make a full release rather than a development release in which case we would remove the following lines from ``setup.cfg``: 

.. code-block:: ini 

    [egg_info] 
    tag_build = dev 
    tag_svn_revision = true 

To test the automatic installation of the dependencies, run the following command which will also install docutils and SQLAlchemy if you don't already have them: 

.. code-block:: bash 

    $ python setup.py develop 

.. Note:: 

    The command ``python setup.py develop`` installs your application in a special mode so that it behaves exactly as if it had been installed as an egg file by an end user. This is really useful when you are developing an application because it saves you having to create an egg and install it every time you want to test a change. 

Configuration and Setup 
======================= 

Now lets make the changes necessary to enable QuickWiki to be set up by an end user. First, open ``environment.py`` from the ``config`` directory of your project. After ``from pylons import config``, add the following import: 

.. code-block:: python 

    from sqlalchemy import engine_from_config 

Then, add this line at the end of the ``load_environment`` function: 

.. code-block:: python 

    config['pylons.app_globals'].sa_engine = \
        engine_from_config(config, 'sqlalchemy.default.') 

This creates an **engine** for each instance of your application, which manages connections and is the base level at which SQLAlchemy communicates with the database. The engine is added to Pylons' ``config`` object, where you earlier saw it accessed in the ``base`` parameter for setting up SQLAlchemy's ``Session``. 

Now edit ``websetup.py``, used by the ``paster setup-app`` command, to look like this: 

.. code-block:: python 

    """Setup the QuickWiki application""" 
    import logging 

    from paste.deploy import appconfig 
    from pylons import config 

    from quickwiki.config.environment import load_environment 

    log = logging.getLogger(__name__) 

    def setup_config(command, filename, section, vars): 
        """Place any commands to setup quickwiki here""" 
        conf = appconfig('config:' + filename) 
        load_environment(conf.global_conf, conf.local_conf) 

    # Populate the DB on 'paster setup-app' 
    import quickwiki.model as model 

    log.info("Setting up database connectivity...") 
    engine = config['pylons.app_globals'].sa_engine 
    log.info("Creating tables...") 
    model.metadata.create_all(bind=engine) 
    log.info("Successfully set up.") 

    log.info("Adding front page data...") 
    page = model.Page() 
    page.title = 'FrontPage' 
    page.content = 'Welcome to the QuickWiki front page.' 
    model.Session.save(page) 
    model.Session.commit() 
    log.info("Successfully set up.") 

You can see that ``environment.py``'s ``load_environment`` function is called, so our engine is ready and we can import the model. A SQLAlchemy ``MetaData`` object--which provides some utility methods for operating on database schema--usually needs to be connected to an engine, so the line ``model.metadata.create_all(bind=engine)`` uses the engine we've set up and, well, creates the table(s) we've defined. After the tables are created the other lines add some data for the simple front page to our wiki. Because we specified ``transactional=True`` when creating our ``Session``, operations will be wrapped in a transaction and committed atomically (unless your DB doesn't support transactions, like MySQL's default MyISAM tables -- but that's beyond the scope of this tutorial). 

To test this functionality run you first need to install your QuickWiki if you haven't already done so in order for ``paster`` to find the version we are developing instead of the version we installed at the very start: 

.. code-block:: bash 

    $ python setup.py develop 

Specify your database URI in ``development.ini`` so that the ``[app:main]`` section contains something like this, customized as needed for your database: 

.. code-block:: ini 

    [app:main] 
    use = egg:QuickWiki 
    ... 
    # Specify the database for SQLAlchemy to use. 
    # %(here) may include a ':' character on Windows environments; this can 
    # invalidate the URI when specifying a SQLite db via path name 
    sqlalchemy.default.url = sqlite:///%(here)s/quickwiki.db 

.. Note:: 

    See the SQLAlchemy note in the `Starting at the End`_ section for information on supported database URIs and a link to the SQLAlchemy documentation about the various options that can be included in them. 

If you want to see the SQL being generated, you can have SQLAlchemy echo it to the console by adding this line: 

.. code-block:: ini 

    sqlalchemy.default.echo = true 

You can now run the ``paster setup-app`` command to setup your tables in the same way an end user would, remembering to drop and recreate the database if the version tested earlier has already created the tables: 

.. code-block:: bash 

    $ paster setup-app development.ini 

At this stage you will need to ensure you have the appropriate Python database drivers for the database you chose, otherwise you might find SQLAlchemy complains it can't get the DBAPI module for the dialect it needs. 

You should also edit ``QuickWiki.egg-info/paste_deploy_config.ini_tmpl`` so that when users run ``paster make-config`` the configuration file that is produced for them will already have a section telling them to enter their own database URI as we did when we installed the finished QuickWiki at the start of the tutorial. Add these lines in the ``[app:main]`` section: 

.. code-block:: ini 

    # Specify the database for SQLAlchemy to use. 
    # %(here) may include a ':' character on Windows environments; this can 
    # invalidate the URI when specifying a SQLite db via path name 
    #sqlalchemy.default.url = sqlite:///%(here)s/quickwiki.db 
    #sqlalchemy.default.echo = true 

Templates 
========= 

.. Note:: 

    Pylons uses the Mako templating language by default, although as is the case with most aspects of Pylons you are free to deviate from the default if you prefer. Pylons also supports Genshi, Kid and Cheetah out of the box. 

We will make use of a feature of the Mako templating language called inheritance for our project. Add the main page template in ``templates/base.mako``: 

.. code-block:: html+mako 

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> 
    <html> 
        <head> 
            <title>QuickWiki</title> 
            ${h.stylesheet_link_tag('/quick.css')} 
            ${h.javascript_include_tag(
                '/javascripts/effects.js', builtins=True)} 
        </head> 
        <body> 
            <div class="content"> 
                ${next.body()}\ 
                <p class="footer"> 
                    Return to the 
                    ${h.link_to('FrontPage', 
                        h.url_for(action="index", title="FrontPage"))} 
                    | ${h.link_to('Edit ' + c.title, 
                        h.url_for(title=c.title, action='edit'))} 
                </p> 
            </div> 
        </body> 
    </html> 

All our other templates will be automatically inserted into the ``${next.body()}`` line and the whole page will be returned when we call the ``render()`` global from our controller so that we can easily apply a consistent theme to all our templates. 

If you are interested in learning some of the features of Mako templates have a look at the comprehensive `Mako Documentation <http://www.makotemplates.org/docs/>`_. For now we just need to understand that next.body() is replaced with the child template and that anything within ``${...}`` brackets is executed and replaced with the result. 

This ``base.mako`` also makes use of various helper functions attached to the ``h`` object. These are described in the `WebHelpers documentation <http://pylonshq.com/WebHelpers/module-index.html>`_. You can add more helpers to the ``h`` object by adding them to ``lib/helpers.py`` although for this project we don't need to do so. 

Routing 
======= 

Before we can add the actions we want to be able to route the requests to them correctly. Edit ``config/routing.py`` and adjust the 'Custom Routes' section to look like this: 

.. code-block:: python 

    map.connect(':controller/:action/:title', controller='page', 
    action='index', title='FrontPage') 
    map.connect(':title', controller='page', action='index', title='FrontPage') 
    map.connect('*url', controller='template', action='view') 

Note that the default route has been replaced. This tells Pylons to route the root URL ``/`` to the ``index()`` method of the ``PageController`` class in ``page.py`` and specify the ``title`` argument as ``FrontPage``. It also says that any URL of the form ``/SomePage`` should be routed to the same method but the ``title`` argument will contain the value of the first part of the URL, in this case ``SomePage``. Any other URLs which can't be matched by these maps are routed to the template controller as usual where they will result in a 404 error page being displayed. 

One of the main benefits of using the Routes system is that you can also create URLs automatically simply by specifying the routing arguments. For example if I want the URL for the page ``FrontPage`` I can create it with this code: 

.. code-block:: python 

    h.url_for(title='FrontPage') 

Although the URL would be fairly simple to create manually, with complicated URLs this approach is much quicker. It also has the significant advantage that if you ever deploy your Pylons application at a URL other than ``/``, all the URLs will be automatically adjusted for the new path without you needing to make any manual modifications. This flexibility is a real advantage. 

Full information on the powerful things you can do to route requests to controllers and actions can be found in the `Routes manual <http://routes.groovie.org/manual.html>`_. 

Controllers 
=========== 

Quick Recap: We've setup the model, configured the application, added the routes and setup the base template in base.mako, now we need to write the application logic and we do this with controllers. In your project's root directory add a controller called ``page`` to your project with this command: 

.. code-block:: bash 

    $ paster controller page 

If you are using Subversion, this will automatically be detected and the new controller and tests will be automatically added to your subversion repository.

We are going to need the following actions: 

``index(self, title)`` 
displays a page based on the title 

``edit(self, title)`` 
displays a from for editing the page ``title`` 

``save(self, title)`` 
save the page ``title`` and show it with a saved message 

``list(self)`` 
gives a list of all pages 

``delete(self)`` 
deletes a page based on an AJAX drag and drop call 

Let's get cracking! We just need to make one quick preparation first: edit the ``BaseController`` class that your new page controller subclasses, so that we get a clean ``Session`` each time one of your controllers is called. Open ``lib/base.py`` and edit the ``__call__`` method like this: 

.. code-block:: python 

    from quickwiki.model import Session 

    class BaseController(WSGIController): 

        def __call__(self, environ, start_response): 
            """Invoke the Controller""" 
            # WSGIController.__call__ dispatches to the Controller method the 
            # request is routed to. This routing information is available in 
            # environ['pylons.routes_dict'] 
            try: 
                return WSGIController.__call__(self, environ, start_response) 
            finally: 
                Session.remove() 

This is critical for avoiding unexpected and hard-to-debug behavior resulting from old session data between requests. 

index() 
------- 

Now we can get to work on the new controller in ``page.py``. First we'll import the Page class from our model class to save some typing later on. Add this line with the imports at the top of the file: 

.. code-block:: python 

    from quickwiki.model import Page 

This is also done the the ``base.py`` file for the Session class, as shown above. This is done sheerly for convenience, and you can instead choose to refer to ``model.Session`` and ``model.Page`` throughout your controllers, since ``BaseController`` imports the model for us. This may help to reduce confusion, especially in more complex applications. 

On to the ``index`` method. Replace the existing ``index()`` action with this: 

.. code-block:: python 

    def index(self, title): 
        page_q = Session.query(Page) 
        page = page_q.filter_by(title=title).first() 
        if page: 
            c.content = page.get_wiki_content() 
            return render('/page.mako') 
        elif model.wikiwords.match(title): 
            return render('/new_page.mako') 
        abort(404) 

Add a template called ``templates/page.mako`` that looks like this: 

.. code-block:: html+mako 

    <%inherit file="base.mako"/> 

    <h1 class="main">${c.title}</h1> 
    ${c.content} 

This template simply displays the page title and content. 

.. Note:: Pylons automatically assigns all the action parameters to the Pylons context object ``c`` so that you don't have to assign them yourself. In this case, the value of ``title`` will be automatically assigned to ``c.title`` so that it can be used in the templates. We assign ``c.content`` manually in the controller. 

We also need a template for pages that don't already exist. It needs to display a message and link to the edit action so that they can be created. Add a template called ``templates/new_page.mako`` that looks like this: 

.. code-block:: html+mako 

    <%inherit file="base.mako"/> 

    <h1 class="main">${c.title}</h1> 
    <p>This page doesn't exist yet. 
    <a href="${h.url_for(action='edit', title=c.title)}">Create the page</a>. 
    </p> 

At this point we can test our QuickWiki to see how it looks. If you don't already have a the server running start it now with: 

.. code-block:: bash 

    $ paster serve --reload development.ini 

Visit http://127.0.0.1:5000/ and you will see the front page of the wiki. If you haven't already done so you should delete the file ``public/index.html`` so that when you visit the URL above you are routed to the correct action in the page controller and see the wiki front page instead of the ``index.html`` file being displayed. 

We can spruce it up a little by adding the stylesheet we linked to in the ``templates/base.mako`` file earlier. Add the file ``public/quick.css`` with the following content and refresh the page to reveal a better looking wiki: 

.. code-block:: css 

    body { 
    background-color: #888; 
    margin: 25px; 
    } 
    div.content{ 
    margin: 0; 
    margin-bottom: 10px; 
    background-color: #d3e0ea; 
    border: 5px solid #333; 
    padding: 5px 25px 25px 25px; 
    } 
    h1.main{ 
    width: 100%; 
    border-bottom: 1px solid #000; 
    } 
    p.footer{ 
    width: 100%; 
    padding-top: 3px; 
    border-top: 1px solid #000; 
    } 

When you run the example you will notice that the word ``QuickWiki`` has been turned into a hyperlink by the ``get_wiki_content()`` method we added to our ``Page`` domain object earlier. You can click the link and will see an example of the new page screen from the ``new_page.mako`` template. If you follow the ``Create the page`` link you will see the Pylons automatic error handler kick in to tell you ``Action edit is not implemented``. Well, we better write it next, but before we do, have a play with the :ref:`interactive_debugging`, try clicking on the ``+`` or ``>>`` arrows and you will be able to interactively debug your application. It is a tremendously useful tool. 

edit() 
------ 

To edit the wiki page we need to get the content from the database without changing it to HTML to display it in a simple form for editing. Add the ``edit()`` action: 

.. code-block:: python 

    def edit(self, title): 
        page_q = Session.query(Page) 
        page = page_q.filter_by(title=title).first() 
        if page: 
            c.content = page.content 
        return render('/edit.mako') 

and then create the ``templates/edit.mako`` file: 

.. code-block:: html+mako  

    <%inherit file="base.mako"/> 

    <h1 class="main">Editing ${c.title}</h1> 

    ${h.start_form(h.url_for(action='save', title=c.title), method="post")} 
    ${h.text_area(name='content', rows=7, cols=40, content=c.content)} <br /> 
    ${h.submit(value="Save changes", name='commit')} 
    ${h.end_form()} 

.. Note:: You might have noticed that we only set ``c.content`` if the page exists but that it is accessed in ``h.text_area`` even for pages that don't exist and yet it doesn't raise an ``AttributeError``. We are making use of the fact that the ``c`` object returns an empty string ``""`` for any attribute that is accessed which doesn't exist. This can be a very useful feature of the ``c`` object, but can catch you on occasions where you don't expect this behavior. It can be disabled by setting ``config['pylons.strict_c'] = True`` in your project's ``config/environment.py``. 

We are making use of the ``h`` object to create our form and field objects. This saves a bit of manual HTML writing. The form submits to the ``save()`` action to save the new or updated content so let's write that next. 

save() 
------ 

The first thing the ``save()`` action has to do is to see if the page being saved already exists. If not it creates it with ``page = model.Page()``. Next it needs the updated content. In Pylons you can get request parameters from form submissions via GET and POST requests from the appropriately named ``request.params`` object. For form submissions from *only* GET or POST requests, use ``request.GET`` or ``request.POST``. Only POST requests should generate side effects (like changing data), so the save action will reference ``request.POST`` for the parameters. 

Add the ``save()`` action: 

.. code-block:: python 

    def save(self, title): 
        page_q = Session.query(Page) 
        page = page_q.filter_by(title=title).first() 
        if not page: 
            page = model.Page() 
        page.title = title 
        page.content = request.POST.get('content','') 
        c.title = page.title 
        c.content = page.get_wiki_content() 
        c.message = 'Successfully saved' 
        Session.save_or_update(page) 
        Session.commit() 
        return render('/page.mako') 

.. Note:: 
    ``request.params``, ``request.GET`` and ``request.POST`` are MultiDict objects: an ordered dictionary that may contain multiple values for each key. The MultiDict will always return one value for any existing key via the normal dict accessors ``request.params[key]`` and ``request.params.get(key)``. When multiple values are expected, use the ``request.params.getall(key)`` method to return all values in a list. 

In order for the ``page.mako`` template to display the ``Successfully saved`` message after the page is saved we need to update the ``templates/page.mako`` file. After ``<h1 class="main">${c.title}</h1>`` add these lines: 

.. code-block:: html+mako 

    % if c.message: 
    <p><div id="message">${c.message}</div></p> 
    % endif 

And add the following to the ``public/quick.css`` file: 

.. code-block:: css 

    div#message{ 
        color: orangered; 
    } 

The ``%`` syntax is used for control structures in mako -- conditionals and loops. You must 'close' them with an 'end' tag as shown here. At this point we have a fully functioning wiki that lets you create and edit pages and can be installed and deployed by an end user with just a few simple commands. 

Visit http://127.0.0.1:5000 and have a play. 

It would be nice to get a title list and to be able to delete pages, so that's what we'll do next! 

list() 
------ 

Add the ``list()`` action: 

.. code-block:: python 

    def list(self): 
        c.titles = [page.title for page in Session.query(Page).all()] 
        return render('/list.mako') 

The ``list()`` action simply gets all the pages from the database. Create the ``templates/list.mako`` file to display the list: 

.. code-block:: html+mako  

    <%inherit file="base.mako"/> 

    <h1 class="main">Title List</h1> 

    <ul id="titles"> 
    % for title in c.titles: 
    <li> 
    ${title}&nbsp;[${h.link_to('visit', h.url_for(title=title, action="index"))}] 
    </li> 
    % endfor 
    </ul> 

Now we need to edit ``templates/base.mako`` to add a link to the title list in the footer, but while we're at it, let's introduce a Mako function to make the footer a little smarter. Edit ``base.mako`` like this: 

.. code-block:: html+mako  

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> 
    <html> 
    <head> 
    <title>QuickWiki</title> 
    ${h.stylesheet_link_tag('/quick.css')} 
    ${h.javascript_include_tag('/javascripts/effects.js', builtins=True)} 
    </head> 
    <body> 
    <div class="content"> 
    ${next.body()}\ 
    <p class="footer"> 
    ${footer(request.environ['pylons.routes_dict']['action'])}\ 
    </p> 
    </div> 
    </body> 
    </html> 

    ## Don't show links that are redundant for particular pages 
    <%def name="footer(action)">\ 
    Return to the ${h.link_to('FrontPage', h.url_for(action="index", title="FrontPage"))} 
    % if action == "list": 
    <% return '' %> 
    % endif 
    % if action != "edit": 
    | ${h.link_to('Edit ' + c.title, h.url_for(title=c.title, action='edit'))} 
    % endif 
    | ${h.link_to('Title List', h.url_for(action='list', title=None))} 
    </%def> 

The ``<%def name="footer(action">`` creates a Mako function for display logic. As you can see, the function builds the HTML for the footer, but doesn't display the 'Edit' link when you're on the 'Title List' page or already on an edit page. It also won't show a 'Title List' link when you're already on that page. The ``<% ... %>`` tags shown on the ``return`` statement are the final new piece of Mako syntax: they're used much like the ``${...}`` tags, but for arbitrary Python code that does not directly render HTML. Also, the double hash (``##``) denotes a single-line comment in Mako. 

So the ``footer`` function is called in place of our old 'static' footer markup. We pass it a value from ``pylons.routes_dict`` which holds the name of the action for the current request. The trailing `\\` character just tells Mako not to render an extra newline. 

If you visit http://127.0.0.1:5000/page/list you should see the full titles list and you should be able to visit each page. 

delete() 
-------- 

Since this tutorial is designed to get you familiar with as much of Pylons core functionality as possible we will use some AJAX to allow the user to drag a title from the title list into a trash area that will automatically delete the page. 

Add this line to ``templates/base.mako`` before ``</head>``: 

.. code-block:: mako 

    ${h.javascript_include_tag('/javascripts/effects.js', builtins=True)} 

.. Note:: The ``h.javascript_include_tag()`` helper will create links to all the built-in JavaScripts we need and also add ``/javascripts/effects.js`` creating HTML that looks like this when you access it from a browser: 

.. code-block:: html 

    <script src="/javascripts/prototype.js" type="text/javascript"></script> 
    <script src="/javascripts/scriptaculous.js" type="text/javascript"></script> 
    <script src="/javascripts/effects.js" type="text/javascript"></script> 

If you look at ``config/middleware.py`` you will see these lines: 

.. code-block:: python 

    javascripts_app = StaticJavascripts() 
    app = Cascade([static_app, javascripts_app, app]) 

The ``javascripts_app`` WSGI application maps any requests to ``/javascripts/`` straight to the relevant JavaScript in the WebHelpers package. This means you don't have to manually copy the Pylons JavaScript files to your project and that if you upgrade Pylons, you will automatically be using the latest scripts.

Now for the AJAX! We want all the titles in the titles list to be draggable so we enclose each of them with a ``<span>`` element with a unique ID. Edit ``templates/list.mako`` to look like this: 

.. code-block:: html+mako  

    <%inherit file="base.mako"/> 

    <h1 class="main">Title List</h1> 

    <ul id="titles"> 
    <%include file="list-titles.mako"/> 
    </ul> 

And then create the new ``templates/list-titles.mako`` as follows: 

.. code-block:: html+mako 

    % for title in c.titles: 
    <li> 
    <span id="${unicode(title)}">${title}</span> 
    &nbsp;[${h.link_to('visit', h.url_for(title=title, action="index"))}] 
    ${h.draggable_element(unicode(title), revert=True)} 
    </li> 
    % endfor 

.. Note:: You can see that we've moved the ``for`` loop into the new template. This is so that we can easily call ``render()`` to update it via AJAX from the delete action that we'll add to our controller in just a moment. We ``<%include />`` this new template in the original ``list.mako``; this is a lot like ``<%inherit />``, but moving downward hierarchically instead of upward. It's perhaps the most basic of templating functions and is much like ``include`` in PHP templating, for example. Notice that ``list-titles.mako`` does not inherit from ``base.mako`` like the others we've created. This way we take maximal advantage of Mako's inheritance, while further reducing code duplication with ``<%include />``. 

We've also added the ``<span>`` tags, and marked each of the titles as a draggable element that reverts to its original position if it isn't dropped over a drop target. If we want to be able to delete the pages we better add a drop target. Try it out at http://127.0.0.1:5000/page/list by dragging the titles themselves around the screen. Notice how much functionality we get with just the one helper ``h.draggable_element()``. 

We better have somewhere to drop the titles to delete them, so add this before the ``<ul id="titles">`` line in ``templates/list.mako`` : 

.. code-block:: html+mako 

    <div id="trash"> 
    Delete a page by dragging its title here 
    </div> 
    ${h.drop_receiving_element("trash", update="titles", url=h.url_for(action="delete"))} 

We will also need to add the style for the trash box to the end of ``public/quick.css``: 

.. code-block:: css 

    div#trash{ 
    float: right; 
    margin: 0px 20px 20px 20px; 
    background: #eee; 
    border: 2px solid #000; 
    padding: 15px; 
    } 

.. Tip:: It can sometimes be very hard to debug AJAX applications. Pylons can help. If an error occurs in debug mode (the default in ``development.ini``) a debug URL where you can use an interactive debugger will be printed to the error stream, even in an AJAX request. If you copy and paste that address into a browser address bar you will be able to debug the request. 

When a title is dropped on the ``trash`` box an AJAX request will be made to the ``delete()`` action, posting an ``id`` parameter with the ``id`` of the element that was dropped. The element with ``id`` ``titles`` will be updated with whatever is returned from the action, so we better add a ``delete()`` action that returns the new list of titles excluding the one that has been deleted: 

.. code-block:: python 

    def delete(self): 
        page_q = Session.query(Page) 
        title = request.POST['id'] 
        page = page_q.filter_by(title=title).one() 
        Session.delete(page) 
        Session.commit() 
        c.titles = page_q.all() 
        return render('/list-titles.mako') 

The title of the page is obtained from the ``id`` element and the object is loaded and then deleted. The change is saved with ``model.Session.commit()`` before the list of remaining titles is re-rendered by the template ``templates/list-titles.mako``. 

Visit http://127.0.0.1:5000/page/list and have a go at deleting some pages. You may need to go back to the FrontPage and create some more if you get carried away! 

That's it! A working, production-ready wiki in 20 mins. You can visit http://127.0.0.1:5000/ once more to admire your work. 

Publishing the Finished Product 
=============================== 

After all that hard work it would be good to distribute the finished package wouldn't it? Luckily this is really easy in Pylons too. In the project root directory run this command: 

.. code-block:: bash 

    $ python setup.py bdist_egg 

This will create an egg file in ``dist`` which contains everything anyone needs to run your program. They can install it with: 

.. code-block:: bash 

    $ easy_install QuickWiki-0.1.5-py2.5.egg 

You should probably make eggs for each version of Python your users might require by running the above commands with both Python 2.4 and 2.5 to create both versions of the eggs. 

If you want to register your project with the Cheeseshop at http://www.python.org/pypi you can run the command below. *Please only do this with your own projects though because QuickWiki has already been registered!* 

.. code-block:: bash 

    $ python setup.py register 

.. Warning:: The CheeseShop authentication is very weak and passwords are transmitted in plain text. Don't use any sign in details that you use for important applications as they could be easily intercepted. 

You will be asked a number of questions and then the information you entered in ``setup.py`` will be used as a basis for the page that is created. 

Now visit http://www.python.org/pypi to see the new index with your new package listed. 

.. Note:: A `CheeseShop Tutorial <http://wiki.python.org/moin/CheeseShopTutorial>`_ has been written and `full documentation on setup.py <http://docs.python.org/dist/dist.html>`_ is available from the Python website. You can even use `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ in the ``description`` and ``long_description`` areas of ``setup.py`` to add formatting to the pages produced on the CheeseShop. There is also `another tutorial here <http://www.python.org/~jeremy/weblog/030924.html>`_. 

Finally you can sign in to the CheeseShop with the account details you used when you registered your application and upload the eggs you've created. If that seems too difficult you can even use this command which should be run for each version of Python supported to upload the eggs for you: 

.. code-block:: bash 

    $ python setup.py bdist_egg upload 

Before this will work you will need to create a ``.pypirc`` file in your home directory containing your username and password so that the ``upload`` command knows who to sign in as. It should look similar to this: 

.. code-block:: ini

    [server-login] 
    username: james 
    password: password 

.. Tip:: This works on windows too but you will need to set your ``HOME`` environment variable first. If your home directory is ``C:\Documents and Settings\James`` you would put your ``.pypirc`` file in that directory and set your ``HOME`` environment variable with this command: 

.. code-block:: bash 

    > SET HOME=C:\Documents and Settings\James 

You can now use the ``python setup.py bdist_egg upload`` as normal. 

Now that the application is on CheeseShop anyone can install it with the ``easy_install`` command exactly as we did right at the very start of this tutorial. 

Security 
======== 

A final word about security. 

.. Danger:: Always set ``debug = false`` in configuration files for production sites and make sure your users do to. 

You should NEVER run a production site accessible to the public with debug mode on. If there was a problem with your application and an interactive error page was shown, the visitor would be able to run any Python commands they liked in the same way you can when you are debugging. This would obviously allow them to do all sorts of malicious things so it is very important you turn off interactive debugging for production sites by setting ``debug = false`` in configuration files and also that you make users of your software do the same. 

Summary 
======= 

We've gone through the whole cycle of creating and distributing a Pylons application looking at setup and configuration, routing, models, controllers and templates. Hopefully you have an idea of how powerful Pylons is and, once you get used to the concepts introduced in this tutorial, how easy it is to create sophisticated, distributable applications with Pylons. 

That's it, I hope you found the tutorial useful. You are encouraged to email any comments to the `Pylons mailing list <http://groups.google.co.uk/group/pylons-discuss>`_ where they will be gratefully received. 

ToDo 
==== 

* If QuickWiki is intended as a reference app for Pylons best practices, I'd like to incorporate some testing into the tutorial. Possibly introduce ``paster shell`` too. 
* Introduce 0.9.6's logging features instead of sqlalchemy.echo 
* Further explain Pylons' Unicode support 

Thanks 
====== 
A big thanks to Ches Martin for updating this document and the QuickWiki project for Pylons 0.9.6/QuickWiki 0.1.5, and others in the Pylons community who contributed bug fixes and suggestions. 

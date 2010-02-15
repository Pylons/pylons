.. _models:

======
Models
======

About the model
===============

.. image:: _static/pylon3.jpg
   :alt: 
   :align: left
   :height: 450px
   :width: 368px

In the MVC paradigm the *model* manages the behavior and data of the application domain, responds to requests for information about its state and responds to instructions to change state.

The model represents enterprise data and business rules. It is where most of the processing takes place when using the MVC design pattern. Databases are in the remit of the model, as are component objects such as :term:`EJBs` and :term:`ColdFusion Components`.

The data returned by the model is display-neutral, i.e. the model applies no formatting. A single model can provide data for any number of display interfaces. This reduces code duplication as model code is written only once and is then reused by all of the views.

Because the model returns data without applying any formatting, the same components can be used with any interface. For example, most data is typically formatted with HTML but it could also be formatted with Macromedia Flash or WAP.

The model also isolates and handles state management and data persistence. For example, a Flash site or a wireless application can both rely on the same session-based shopping cart and e-commerce processes.

Because the model is self-contained and separate from the controller and the view, changing the data layer or business rules is less painful. If it proves necessary to switch databases, e.g. from MySQL to Oracle, or change a data source from an RDBMS to LDAP, the only required task is that of altering the model. If the view is written correctly, it won’t care at all whether a list of users came from a database or an LDAP server.

This freedom arises from the way that the three parts of an MVC-based application act as `black boxes`, the inner workings of each one are hidden from, and are independent of, the other two. The approach promotes well-defined interfaces and self-contained components.

.. note:: *adapted from an Oct 2002 TechRepublic article by by Brian Kotek: "MVC design pattern brings about better organization and code reuse"* - http://articles.techrepublic.com.com/5100-10878_11-1049862.html

Model Basics
============

Pylons provides a :data:`model` package to put your database code in but does not offer a database engine or API.  Instead there are several third-party APIs to choose from.

The recommended and most commonly-adopted approach used in Pylons applications is to use SQLAlchemy with the declarative configuration style and develop with a relational database (Postgres, MySQL, etc). 

**This is the documented and recommended approach for creating a Pylons project with a SQL database**.

Install SQLAlchemy
------------------

We'll assume you've already installed Pylons and have the `easy_install` command. At the command line, run: 

.. code-block:: bash

    easy_install SQLAlchemy 


Next you'll have to install a database engine and its Python bindings. If you don't know which one to choose, SQLite is a good one to start with. It's small and easy to install, and Python 2.5 includes bindings for it. Installing the database engine is beyond the scope of this article, but here are the Python bindings you'll need for the most popular engines: 

.. code-block:: bash

    easy_install pysqlite # If you use SQLite and Python 2.4 (not needed for Python 2.5) 
    easy_install MySQL-python # If you use MySQL 
    easy_install psycopg2 # If you use PostgreSQL 


See the `Python Package Index <http://pypi.python.org/>`_ (formerly the Cheeseshop) for other database drivers. 

.. tip:: Checking Your Version

    To see which version of SQLAlchemy you have, go to a Python shell and look at ``sqlalchemy.__version__`` :
    
    .. code-block:: pycon

        >>> import sqlalchemy 
        >>> sqlalchemy.__version__ 
        0.5.8

Create a Pylons Project with SQLAlchemy
---------------------------------------

When creating a Pylons project, one of the questions asked as part of the project creation dialogue is whether the project should be configured with SQLAlchemy. Before continuing, ensure that the project was created with this option, if it's missing the :file:`model/meta.py` file, then the project should be re-created with this option.
    
.. tip::
    
    The project doesn't need to be deleted to add this option, just re-run
    the `paster` command in the project's parent directory and answer "yes"
    to the SQLAlchemy prompt. The files will then be added and existing
    files will present a prompt on whether to replace them or leave the
    current file.

Configure SQLAlchemy
--------------------

When your Pylons application runs, it needs to know which database to connect to. Normally you put this information in *development.ini* and activate the model in *environment.py*: put the following in *development.ini* in the `\[app:main\]` section, depending on your database, 

For SQLite 
^^^^^^^^^^


.. code-block:: ini

    sqlalchemy.url = sqlite:///%(here)s/mydatabasefilename.sqlite 


Where `mydatabasefilename.db` is the path to your SQLite database file. "%(here)s" represents the directory containing the development.ini file. If you're using an absolute path, use four slashes after the colon: "sqlite:////var/lib/myapp/database.sqlite". Don't use a relative path (three slashes) because the current directory could be anything. The example has three slashes because the value of "%(here)s" always starts with a slash (or the platform equivalent; e.g., "C:\\foo" on Windows). 

For MySQL 
^^^^^^^^^

.. code-block:: ini

    sqlalchemy.url = mysql://username:password@host:port/database 
    sqlalchemy.pool_recycle = 3600 

Enter your username, password, host (localhost if it is on your machine), port number (usually 3306) and the name of your database. The second line is an example of setting `engine options <http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_options>`_. 

It's important to set "pool_recycle" for MySQL to prevent "MySQL server has gone away" errors. This is because MySQL automatically closes idle database connections without informing the application. Setting the connection lifetime to 3600 seconds (1 hour) ensures that the connections will be expired and recreated before MySQL notices they're idle. 

Don't be tempted to use the ".echo" option to enable SQL logging because it may cause duplicate log output. Instead see the `Logging`_ section below to integrate MySQL logging into Paste's logging system. 

For PostgreSQL 
^^^^^^^^^^^^^^

.. code-block:: ini

    sqlalchemy.url = postgres://username:password@host:port/database 


Enter your username, password, host (localhost if it is on your machine), 
port number (usually 5432) and the name of your database. 


Organizing
==========

When you answer "yes" to the SQLAlchemy question when creating a Pylons
project, it configures a simple default model.  The model consists of two
files: :file:`model/__init__.py` and :file:`model/meta.py`.

:file:`model/__init__.py`
-------------------------
The file :file:`model/__init__.py` contains the table definitions, the ORM 
classes and an :func:`init_model` function. This :func:`init_model` function 
must be called at application startup. In the Pylons default project template
this call is made in the :func:`load_environment` function (in the file 
:file:`config/environment.py`).

:file:`model/meta.py`
---------------------
:file:`model/meta.py` is merely a container for a few housekeeping objects 
required by SQLAlchemy such as :class:`Session`, ``metadata`` and ``engine``
to avoid import issues. In the context of the default Pylons application, only
the :class:`Session` object is instantiated. 

The objects are optional in the context of other applications that do not make 
use of them and so if you answer "no" to the SQLAlchemy question when creating 
a Pylons project, the creation of :file:`model/meta.py` is simply skipped.

It is recommended that, for each model, a new module inside the ``model/``
directory should be created. This keeps the models tidy when they get 
larger as more domain specific code is added to each one.

Creating a Model
================

SQLAlchemy 0.5 has an optional `Declarative` syntax which offers the 
convenience of defining the table and the ORM class in one step. This
is the recommended usage of SQLAlchemy.

Create a :file:`model/person.py` module::

    """Person model"""
    from sqlalchemy import Column
    from sqlalchemy.types import Integer, String

    from myapp.model.meta import Base

    class Person(Base):
        __tablename__ = "person"

        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        email = Column(String(100))
        
        def __init__(self, name='', email=''):
            self.name = name
            self.email = email
        
        def __repr__(self):
            return "<Person('%s')" % self.name

.. note::
    
    ``Base`` is imported from :file:`model/meta.py` to prevent recursive
    import problems when added to :file:`model/__init__.py` in the next
    step.

Then for convenience when using the models, import it in :file:`model/__init__.py`::
    
    """The application's model objects"""
    from myapp.model.meta import Session, Base
    
    from myapp.model.person import Person

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        Session.configure(bind=engine)

Adding a Relation
=================

Here's an example of a :class:`Person` and an :class:`Address` class with a 
one-to-many relationship on `person.addresses`.

First, add a :file:`model/address.py` module::
    
    """Address model"""
    from sqlalchemy import Column, ForeignKey
    from sqlalchemy.types import Integer, String
    from sqlalchemy.orm import relation, backref

    from myapp.model.meta import Base

    class Address(Base):
        __tablename__ = "address"

        id = Column(Integer, primary_key=True)
        address = Column(String(100))
        city = Column(String(100))
        state = Column(String(2))
        person_id = Column(Integer, ForeignKey('person.id'))
        
        person = relation('Person', backref=backref('addresses', order_by=id))

        def __repr__(self):
            return "<Person('%s')" % self.name

When models are created using the declarative ``Base``, each one is added by
name to a mapping. This allows the ``relation`` option above to locate the
model it should be related to based on the text string ``'Person'``.

Then add the import to the :file:`model/__init__.py` file::
    
    """The application's model objects"""
    from myapp.model.meta import Session, Base
    
    from myapp.model.address import Address
    from myapp.model.person import Person

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        Session.configure(bind=engine)


.. seealso::
    `Building a Relation <http://www.sqlalchemy.org/docs/05/ormtutorial.html#building-a-relation>`_
    and 
    `SQLAlchemy manual`_

Creating the Database
=====================

To actually create the tables in the database, you call the metadata's `.create_all()` method. You can do this interactively or use `paster`'s application initialization feature. To do this, put the code in :file:`myapp/websetup.py`. After the `load_environment()` call, put: 

.. code-block:: python

    from myapp.model.meta import Base, Session
    log.info("Creating tables")
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")

Then run the following on the command line: 

.. code-block:: bash

    $ paster setup-app development.ini

A brief guide to using model objects in the Controller
======================================================

In which we: query a model, update a model entity, create a model entity and delete several model entities, all inside a Pylons controller.

To illustrate some typical ways of handling model objects in the Controller, we will draw from the example :class:`PagesController` code of the :ref:`QuickWiki Tutorial`.

The :class:`Session`
--------------------

The SQLAlchemy-provided :class:`Session` object is a crucially important facet when working with models and model object entities.

The SQLAlchemy documentation describes the :class:`Session` thus: "In the most general sense, the Session establishes all conversations with the database and represents a "holding zone" for all the mapped instances which you’ve loaded or created during its lifespan."

All of the model access that takes place in a Pylons controller is done in the context of a :class:`Session` providing a database connection reference that is created at the start of the processing of each request and destroyed at the end of the processing of the request.

These creation and destruction operations are performed automatically by the :class:`BaseController` instantiated in :file:`MYAPP/lib/base.py` which is in turn subclassed for each standard Pylons controller, ensuring that subclassed controllers can access the database only in a request-specific context which, in turn, protects against data accidentally leaking across requests.

.. seeAlso:: 
    SQLAlchemy documentation for the `Session object <http://www.sqlalchemy.org/docs/session.html>`_

The net effect of this is that a fully-instantiated :class:`Session` object is available for import and immediate use in the controller for, e.g. querying the model.

Querying the model
------------------

The :class:`Session` object provides a :func:`query` function that, when applied to a class of mapped model object, returns a SQLAlchemy :class:`Query` object that can be passed around and repeatedly consulted.

.. seealso:: 
        SQLAlchemy documentation for the `Query object <http://www.sqlalchemy.org/docs/reference/orm/query.html>`_

Standard usage is illustrated in this code for the :func:`__before__` function of the QuickWiki :class:`PagesController` in which ``self.page_q`` is bound to the :class:`Query` object returned by ``Session.query(Page)`` - where :class:`Page` is the class of mapped model object that will be the subject of the queries.

.. code-block:: python

    from MYAPP.lib.base import Session
    from MYAPP.model import Page

    class PagesController(BaseController):

        def __before__(self):
            self.page_q = Session.query(Page)

        # [ ... ]

The :class:`Query` object that is bound to ``self.page_q`` is now specialised to perform queries of the :class:`Page` declarative base entity / mapped model entity. 

.. seeAlso:: 
        SQLAlchemy documentation for the `Querying the database <http://www.sqlalchemy.org/docs/ormtutorial.html#querying>`_

Here, in the context of a controller's :func:`index` action, it is used in a very straighforward manner - :func:`self.page_q.all` - to fuel a list comprehension that returns a list containing the ``title`` of every :class:`Page` object in the database:

.. code-block:: python

    def index(self):
        c.titles = [page.title for page in self.page_q.all()]
        return render('/pages/index.mako')

and ``self.page_q`` is used in similarly direct manner for the :func:`show` action that retrieves a Page with a given value of ``title`` and then calls the Page's  :func:`get_wiki_content` class method. 

.. code-block:: python

    def show(self, title):
        page = self.page_q.filter_by(title=title).first()
        if page:
            c.content = page.get_wiki_content()
            return render('/pages/show.mako')
        elif wikiwords.match(title):
            return render('/pages/new.mako')
        abort(404)

.. note:: the ``title`` argument to the function is bound when the request is dispatched by the Routes map, typically of the form:

    .. code-block:: python

        map.connect('show_page', '/page/show/{title}', controller='page', action='show')

The :class:`Query` object has many other features, including filtering on conditions, ordering the results, grouping, etc. These are excellently described in the `SQLAlchemy manual`_. See especially the `Data Mapping <http://www.sqlalchemy.org/docs/datamapping.html>`_ and `Session / Unit of Work <http://www.sqlalchemy.org/docs/unitofwork.html>`_ chapters. 


Creating, updating and deleting model entities
----------------------------------------------

When performing operations that change the state of the database, the recommended approach is for Pylons users to take full advantage of the abstraction provided by the SQLAlchemy ORM and simply treat the retrieved or created model entities as Python objects, make changes to them in a conventional Pythonic way, add them to or delete them from the :class:`Session` "holding zone" and call :func:`Session.commit` to commit the changes to the database.

The three examples shown below are condensed illustrations of how these operations are typically performed in controller actions.

Creating a model entity
^^^^^^^^^^^^^^^^^^^^^^^

SQLAlchemy's Declarative Base syntax allows model entity classes to act as constructors, accepting keyworded args and values. In this example, a new Page is created with the given title, the created model entity object is then added to the :class:`Session` and then the change is committed.

.. code-block:: python

    def create(self, title):
        page = Page(title=title)
        Session.add(page)
        Session.commit()
        redirect_to('show_page', title=title)

Updating a model entity
^^^^^^^^^^^^^^^^^^^^^^^

Perhaps the most straighforward use - a model entity object is retrieved from the database, a field value is updated and the change committed. 

(Note, this example is considerably abbreviated as a controller action - preliminary content checking has been omitted, as has exception handling for the database query.)

.. code-block:: python

    def save(self, title):
        page = self.page_q.filter_by(title=title).first()
        page.content=escape(request.POST.getone('content'))
        Session.commit()
        redirect_to('show_page', title=title)

Deleting a model entity
^^^^^^^^^^^^^^^^^^^^^^^

This example of shows the freedom that the Pylons user has to make repeated changes to the model (in this instance, repeatedly deleting entities from the database) before finally committing those changes by calling :func:`Session.commit`.

.. code-block:: python

    def delete(self):
        titles = request.POST.getall('title')
        pages = self.page_q.filter(Page.title.in_(titles))
        for page in pages:
            Session.delete(page)
        Session.commit()
        redirect_to('pages')

The `Object Relational tutorial <http://www.sqlalchemy.org/docs/ormtutorial.html>`_ in the SQLAlchemy documentation covers a basic SQLAlchemy object-relational mapping scenario in much more detail and the `SQL Expression tutorial <http://www.sqlalchemy.org/docs/sqlexpression.html>`_ covers the details of manipulating and marshalling the model entity objects.


Using multiple databases
------------------------

In order to use multiple databases, in :file:`MYAPP/model/meta.py` create as many instances of :class:`Base` as there are databases to connect to:

.. code-block:: python

    """SQLAlchemy Metadata and Session object"""
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker

    __all__ = ['Base','Base2', 'Session']

    # SQLAlchemy session manager. Updated by model.init_model()
    Session = scoped_session(sessionmaker())

    # The declarative Base
    Base = declarative_base()
    Base2 = declarative_base()

Declare the different database URLs in :file:`development.ini`, appending an integer to the ``sqlalchemy`` keyword in order to differentiate between them.

.. code-block:: ini

    sqlalchemy.url = sqlite:///%(here)s/database_one.sqlite
    sqlalchemy.echo = true
    sqlalchemy2.url = sqlite:///%(here)s/database_two.sqlite
    sqlalchemy2.echo = false

In :file:`MYAPP/config/environment.py`, pick up those db URL declarations by using the different keywords (in this example: `sqlalchemy` and `sqlalchemy2`). Create the engines and call :func:`model.init_model`, passing through both engines as parameters.

.. code-block:: python

    # Setup the SQLAlchemy database engine
    # Engine 0
    engine = engine_from_config(config, 'sqlalchemy.')
    engine2 = engine_from_config(config, 'sqlalchemy2.')
    model.init_model(engine, engine2)

Bind the engines appropriately to the :class:`Base`-specific metadata in :file:`MYAPP/model/\_\_init\_\_.py` - note :func:`init_model` is expecting both engines to be supplied as formal parameters.

.. code-block:: python

    def init_model(engine, engine2):
        meta.Base.metadata.bind = engine
        meta.Base2.metadata.bind = engine2

Then import :class:`Base` and/or :class:`Base2`

.. code-block:: python

    from MYAPP.model.meta import Base, Base2

and use as required, e.g.

.. code-block:: python

    class Author(Base2):
        __tablename__ = 'authors'
        id = Column(Integer, primary_key=True)
        keywords = relation("Keyword", secondary=keywords)

Avoiding the "circular imports" problem of model interdependency
----------------------------------------------------------------

Closely-interdependent models can sometimes cause "circular import" problems, where importing one model file causes a dependent model file to be imported, which then cause the first model file to be imported, and so on round and round in circles.

In order to break the circle, define the model entities as globals in  :file:`MYAPP/model/meta.py`

.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from MYAPP.model import meta
    from sqlalchemy.orm import scoped_session, sessionmaker

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        meta.Base.metadata.bind = engine
    
        import MYAPP.model.user
        User = MYAPP.model.user.User
        global User
    
        import MYAPP.model.newsletter
        Newsletter = MYAPP.model.newsletter.Newsletter
        global Newsletter
    
        import MYAPP.model.submission
        Submission = MYAPP.model.submission.Submission
        global Submission


Testing the Models
------------------

Normal model usage works fine in model tests, however to use the metadata you must specify an engine connection for it. To have your tables created for every unit test in your project, use a :file:`test_models.py` such as: 

.. code-block:: python

    from myapp.tests import * 
    from myapp import model 
    from myapp.model import meta 

    class TestModels(TestController):

        def setUp(self): 
            meta.Session.remove() 
            meta.Base.metadata.create_all(meta.engine) 

        def test_index(self): 
            # test your models 
            pass


.. note:: Notice that the tests inherit from TestController. This is to ensure that the application is setup so that the models will work. 


"nosetests --with-pylons=/path/to/test.ini ..." is another way to ensure that your model is properly initialized before the tests are run. This can be used when running non-controller tests. 

Logging
=======

SQLAlchemy has several loggers that chat about the various aspects of its operation. To log all SQL statements executed along with their parameter values, put the following in :file:`development.ini`: 

.. code-block:: ini

    [logger_sqlalchemy] 
    level = INFO
    handlers = 
    qualname = sqlalchemy.engine 

Then modify the "[loggers]" section to enable your new logger: 

.. code-block:: ini

    [loggers] 
    keys = root, myapp, sqlalchemy 


To log the results along with the SQL statements, set the level to DEBUG. This can cause a lot of output! To stop logging the SQL, set the level to WARN or ERROR. 

SQLAlchemy has several other loggers you can configure in the same way. "sqlalchemy.pool" level INFO tells when connections are checked out from the engine's connection pool and when they're returned. "sqlalchemy.orm" and buddies log various ORM operations. See "Configuring Logging" in the `SQLAlchemy manual`_. 

About SQLAlchemy
================

`SQLAlchemy <http://www.sqlalchemy.org/>`_ is by far the most common approach for Pylons databases.  It provides a connection pool, a SQL statement builder, an object-relational mapper (ORM), and transaction support.  SQLAlchemy works with several database engines (MySQL, PostgreSQL, SQLite, Oracle, Firebird, MS-SQL, Access via ODBC, etc) and understands the peculiar SQL dialect of each, making it possible to port a program from one engine to another by simply changing the connection string.  Although its API is still changing gradually, SQLAlchemy is well tested, widely deployed, has excellent documentation, and its mailing list is quick with answers.

SQLAlchemy lets you work at three different levels, and you can even use
multiple levels in the same program:

* The object-relational mapper (ORM) lets you interact with the database using your own object classes rather than writing SQL code. 
* The SQL expression language has many methods to create customized SQL statements, and the result cursor is more friendly than DBAPI's. 
* The low-level execute methods accept literal SQL strings if you find something the SQL builder can't do, such as adding a column to an existing table or modifying the column's type. If they return results, you still get the benefit of SQLAlchemy's result cursor. 

The first two levels are *database neutral*, meaning they hide the differences between the databases' SQL dialects. Changing to a different database is merely a matter of supplying a new connection URL. Of course there are limits to this, but SQLAlchemy is 90% easier than rewriting all your SQL queries. 

The `SQLAlchemy manual`_ should be your next stop for questions not covered here. It's very well written and thorough.

SQLAlchemy add-ons
------------------

Most of these provide a higher-level ORM, either by combining the table definition and ORM class definition into one step, or supporting an "active record" style of access.  

*Please take the time to learn how to do things "the regular way" before using these shortcuts in a production application*.  

Understanding what these add-ons do behind the scenes will help if you have to troubleshoot a database error or work around a limitation in the add-on later.

`SQLSoup <http://www.sqlalchemy.org/docs/05/plugins.html#plugins_sqlsoup>`_, an extension to SQLAlchemy, provides a quick way to generate ORM classes based on existing database tables.

If you're familiar with ActiveRecord, used in Ruby on Rails, then you may want to use the `Elixir <http://elixir.ematia.de/>`_ layer on top of SQLAlchemy. This approach is less common since the introduction of the declarative extension, but has other features the declarative does not.

.. _`SQLAlchemy manual`: http://www.sqlalchemy.org/docs/

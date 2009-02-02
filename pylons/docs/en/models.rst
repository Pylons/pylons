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

Model basics
============

Pylons provides a :data:`model` package to put your database code in but does not offer a database engine or API.  Instead there are several third-party APIs to choose from.

SQL databases
-------------

SQLAlchemy
^^^^^^^^^^

`SQLAlchemy <http://www.sqlalchemy.org/>`_ is by far the most common approach for Pylons databases.  It provides a connection pool, a SQL statement builder, an object-relational mapper (ORM), and transaction support.  SQLAlchemy works with several database engines (MySQL, PostgreSQL, SQLite, Oracle, Firebird, MS-SQL, Access via ODBC, etc) and understands the peculiar SQL dialect of each, making it possible to port a program from one engine to another by simply changing the connection string.  Although its API is still changing gradually, SQLAlchemy is well tested, widely deployed, has excellent documentation, and its mailing list is quick with answers.  :ref:`Using SQLAlchemy <working_with_sqlalchemy>` describes the recommended way to configure a Pylons application for SQLAlchemy.

SQLAlchemy lets you work at three different levels, and you can even use
multiple levels in the same program:

* The object-relational mapper (ORM) lets you interact with the database using your own object classes rather than writing SQL code. 
* The SQL expression language has many methods to create customized SQL statements, and the result cursor is more friendly than DBAPI's. 
* The low-level execute methods accept literal SQL strings if you find something the SQL builder can't do, such as adding a column to an existing table or modifying the column's type. If they return results, you still get the benefit of SQLAlchemy's result cursor. 

The first two levels are *database neutral*, meaning they hide the differences between the databases' SQL dialects. Changing to a different database is merely a matter of supplying a new connection URL. Of course there are limits to this, but SQLAlchemy is 90% easier than rewriting all your SQL queries. 

The `SQLAlchemy manual <http://www.sqlalchemy.org/docs/>`_ should be your next stop for questions not covered here. It's very well written and thorough.

SQLAlchemy add-ons
^^^^^^^^^^^^^^^^^^

Most of these provide a higher-level ORM, either by combining the table definition and ORM class definition into one step, or supporting an "active record" style of access.  
*Please take the time to learn how to do things "the regular way" before using these shortcuts in a production application*.  Understanding what these add-ons do behind the scenes will help if you have to troubleshoot a database error or work around a limitation in the add-on later.

`SQLSoup <http://www.sqlalchemy.org/docs/05/plugins.html#plugins_sqlsoup>`_, an extension to SQLAlchemy, provides a quick way to generate ORM classes based on existing database tables.

If you're familiar with ActiveRecord, used in Ruby on Rails, then you may want to use the `Elixir <http://elixir.ematia.de/>`_ layer on top of SQLAlchemy.

`Tesla <http://code.google.com/p/tesla-pylons-elixir/>`_ is a framework built on top of Pylons and Elixir/SQLAlchemy.

Non-SQLAlchemy libraries
^^^^^^^^^^^^^^^^^^^^^^^^

Most of these expose only the object-relational mapper; their SQL builder and connection pool are not meant to be used directly.

`Storm <http://storm.canonical.com>`_

DB-API
++++++

All the SQL libraries above are built on top of Python's DB-API, which provides a common low-level interface for interacting with several database engines: MySQL, PostgreSQL, SQLite, Oracle, Firebird, MS-SQL, Access via ODBC, etc.  Most programmers do not use DB-API directly because its API is low-level and repetitive and does not provide a connection pool.  There's no "DB-API package" to install because it's an abstract interface rather than software.  Instead, install the Python package for the particular engine you're interested in.  Python's `Database Topic Guide <http://www.python.org/topics/database/>`_ describes the DB-API and lists the package required for each engine.  The `sqlite3 <http://docs.python.org/lib/module-sqlite3.html>`_ package for SQLite is included in Python 2.5.

Object databases
----------------

Object databases store Python dicts, lists, and classes in pickles, allowing you to access hierarchical data using normal Python statements rather than having to map them to tables, relations, and a foreign language (SQL).

`ZODB <http://wiki.zope.org/ZODB/FrontPage>`_

`Durus <http://www.mems-exchange.org/software/durus/>`_ [#]_

.. [#] Durus is not thread safe, so you should use its server mode if your
   application writes to the database.  Do not share connections between
   threads.  ZODB is thread safe, so it may be a more convenient alternative.

Other databases
---------------

Pylons can also work with other database systems, such as the following:

`Schevo <http://schevo.org/>`_ uses Durus to combine some features of relational and object databases.  It is written in Python.

`CouchDb <http://couchdb.org/>`_ is a document-based database.  It features a `Python API <http://code.google.com/p/couchdb-python/>`_.

The Datastore database in Google App Engine.

.. _working_with_sqlalchemy:

Working with SQLAlchemy
=======================

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

Check Your Version 
^^^^^^^^^^^^^^^^^^


To see which version of SQLAlchemy you have, go to a Python shell and look at sqlalchemy.\_\_version\_\_ : 

.. code-block:: python

    >>> import sqlalchemy 
    >>> sqlalchemy.__version__ 
    0.5.0


Defining tables and ORM classes
-------------------------------

When you answer "yes" to the SQLAlchemy question when creating a Pylons
project, it configures a simple default model.  The model consists of two
files: *__init__.py* and *meta.py*.  *__init__.py* contains your table
definitions and ORM classes, and an ``init_model()`` function which must be
called at application startup.  *meta.py* is merely a container for
SQLAlchemy's housekeeping objects (``Session``, ``metadata``, and ``engine``),
which not all applications will use.  If your application is small, you can put
your table definitions in *__init__.py* for simplicity.  If your
application has many tables or multiple databases, you may prefer to split them
up into multiple modules within the model.

As of the Pylons 0.9.7 release, SQLAlchemy 0.4.8 is the current production
version, while SQLAlchemy 0.5rc4 is the almost-released new version.  The
default Pylons model was written for SQLAlchemy 0.4, but also works on 0.5 with
a slight change to the *sessionmaker* arguments.  
Here's a sample *model/__init__.py* with a "persons" table, which is based on
the default model with the comments removed:

.. code-block:: python

    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    from myapp.model import meta

    def init_model(engine):
        sm = orm.sessionmaker(transactional=True, autoflush=True, bind=engine)
        meta.Session = orm.scoped_session(sm)
        meta.engine = engine

    t_persons = sa.Table("persons", meta.metadata,
        sa.Column("id", sa.types.Integer, primary_key=True),
        sa.Column("name", sa.types.String(100), primary_key=True),
        sa.Column("email", sa.types.String(100),
        )

    class Person(object):
        pass

    orm.mapper(Person, t_persons)

SQLAlchemy 0.5 users should change the *sessionmaker* line to this:

.. code-block:: python

    sm = orm.sessionmaker(bind=engine)

This model has one table, "persons", assigned to the variable ``t_persons``.
``Person`` is an ORM class which is tied to the table via the mapper.

If the table already exists, you can read its column definitions from the
database rather than specifying them manually; this is called *reflecting* the
table.  The advantage is you don't have to specify the column types in Python
code.  Reflecting must be done inside ``init_model()`` because it depends on a
live database engine, which is not available when the module is imported.  (An
*engine* is a SQLAlchemy object that knows how to connect to a particular
database.)  Here's the second example with reflection:

.. code-block:: python

    import sqlalchemy as sa
    import sqlalchemy.orm as orm

    from myapp.model import meta

    def init_model(engine):
        global t_persons

        sm = orm.sessionmaker(transactional=True, autoflush=True, bind=engine)
        meta.Session = orm.scoped_session(sm)
        meta.engine = engine

        t_persons = sa.Table(meta.metadata, autoload=True, autoload_with=engine)

        orm.mapper(Person, t_persons)

    class Person(object):
        pass

Note how ``t_persons`` and the ``orm.mapper()`` call moved into ``init_model``,
while the ``Person`` class didn't have to.  Also note the ``global t_persons``
statement.  This tells Python that ``t_persons`` is a global variable outside
the function.  ``global`` is required when assigning to a global variable
inside a function.  It's not required if you're merely modifying a mutable
object in place, which is why ``meta`` doesn't have to be declared global.

SQLAlchemy 0.5 has an optional Declarative syntax which defines the table and
the ORM class in one step:

.. code-block:: python

    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    import sqlalchemy.ext.declarative as declarative

    from myapp.model import meta

    _Base = declarative_base()

    def init_model(engine):
        sm = orm.sessionmaker(bind=engine)
        meta.Session = orm.scoped_session(sm)
        meta.engine = engine

    class Person(_Base):
        __tablename__ = "persons"

        id = sa.Column(sa.types.Integer, primary_key=True)
        name = sa.Column(sa.types.String(100))
        email = sa.Column(sa.types.String(100))

A full summary of changes in SQLAlchemy 0.5 and upgrade instructions is at
http://www.sqlalchemy.org/trac/wiki/05Migration .

Relation example 
^^^^^^^^^^^^^^^^


Here's an example of a `Person` and an `Address` class with a many:many relationship on `people.my_addresses`. See `Relational Databases for People in a Hurry <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_ and the SQLAlchemy manual for details. 

.. code-block:: python

    t_people = sa.Table('people', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('name', sa.types.String(100)), 
        sa.Column('email', sa.types.String(100)),
        ) 

    t_addresses_people = sa.Table('addresses_people', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('person_id', sa.types.Integer, sa.ForeignKey('people.id')), 
        sa.Column('address_id', sa.types.Integer, sa.ForeignKey('addresses.id')),
        ) 

    t_addresses = sa.Table('addresses', meta.metadata, 
        sa.Column('id', sa.types.Integer, primary_key=True), 
        sa.Column('address', sa.types.String(100)),
        ) 

    class Person(object): 
        pass 

    class Address(object): 
        pass 

    orm.mapper(Address, t_addresses) 
    orm.mapper(Person, t_people, properties = { 
        'my_addresses' : orm.relation(Address, secondary = t_addresses_people), 
        }) 


Using the model standalone 
^^^^^^^^^^^^^^^^^^^^^^^^^^

You now have everything necessary to use the model in a standalone script such as a cron job, or to test it interactively. You just need to create a SQLAlchemy engine and connect it to the model. This example uses a database "test.sqlite" in the current directory: 

.. code-block:: python

    % python 
    Python 2.5.1 (r251:54863, Oct 5 2007, 13:36:32) 
    [GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2 
    Type "help", "copyright", "credits" or "license" for more information. 
    >>> import sqlalchemy as sa 
    >>> engine = sa.create_engine("sqlite:///test.sqlite") 
    >>> from myapp import model 
    >>> model.init_model(engine) 

Now you can use the tables, classes, and Session as described in the SQLAlchemy
manual.  For example:

.. code-block:: python

    #!/usr/bin/env python
    import sqlalchemy as sa
    import tmpapp.model as model
    import tmpapp.model.meta as meta

    DB_URL = "sqlite:///test.sqlite" 

    engine = sa.create_engine(DB_URL)
    model.init_model(engine)

    # Create all tables, overwriting them if they exist.
    if hasattr(model, "_Base"):
        # SQLAlchemy 0.5 Declarative syntax
        model._Base.metadata.drop_all(bind=engine, checkfirst=True)
        model._Base.metadata.create_all(bind=engine)
    else:
        # SQLAlchemy 0.4 and 0.5 syntax without Declarative
        meta.metadata.drop_all(bind=engine, checkfirst=True)
        meta.metadataa.create_all(bind=engine)

    # Create two records and insert them into the database using the ORM.
    a = model.Person()
    a.name = "Aaa"
    a.email = "aaa@example.com"
    meta.Session.save(a)

    b = model.Person()
    b.name = "Bbb"
    b.email = "bbb@example.com"
    meta.Session.save(b)

    meta.Session.commit()

    # Display all records in the persons table.
    print "Database data:"
    for p in meta.Session.query(model.Person):
        print "id:", p.id
        print "name:", p.name
        print "email:", p.email
        print



The config file
---------------

When your Pylons application runs, it needs to know which database to connect to. Normally you put this information in *development.ini* and activate the model in *environment.py*. Put the following in *development.ini* in the `\[app:main\]` section, depending on your database, 

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

Don't be tempted to use the ".echo" option to enable SQL logging because it may cause duplicate log output. Instead see the "Logging" section below to integrate MySQL logging into Paste's logging system. 

For PostgreSQL 
^^^^^^^^^^^^^^


.. code-block:: ini

    sqlalchemy.url = postgres://username:password@host:port/database 


Enter your username, password, host (localhost if it is on your machine), port number (usually 5432) and the name of your database. 

The engine
----------


Put this at the top of *myapp/config/environment.py*: 

.. code-block:: python

    from sqlalchemy import engine_from_config 
    from myapp.model import init_model 


And this in the `load_environment` function: 

.. code-block:: python

    engine = engine_from_config(config, 'sqlalchemy.') 
    init_model(engine) 


The second argument is the prefix to look for. If you named your keys "sqlalchemy.default.url", you would put "sqlalchemy.default." here. The prefix may be anything, as long as it's consistent between the config file and this function call. 

Controller
----------


Add the following to the top of *myapp/lib/base.py* (the base controller): 

.. code-block:: python

    from myapp.model import meta 


And change the `.\_\_call\_\_` method to: 
.. code-block:: python

    def __call__(self, environ, start_response): 
        try: 
            return WSGIController.__call__(self, environ, start_response) 
        finally: 
            meta.Session.remove() 


The .remove() method is so that any leftover ORM data in the current web request is discarded. This usually happens automatically as a product of garbage collection but calling .remove() ensures this is the case.

Building the database
---------------------


To actually create the tables in the database, you call the metadata's `.create_all()` method. You can do this interactively or use `paster`'s application initialization feature. To do this, put the code in *myapp/websetup.py*. After the `load_environment()` call, put: 

.. code-block:: python

    from myapp.model import meta 
    log.info("Creating tables") 
    meta.metadata.drop_all(bind=meta.engine, checkfirst=True)
    meta.metadata.create_all(bind=meta.engine) 
    log.info("Successfully setup") 

Or for SQLAlchemy 0.5 with the Declarative syntax:

.. code-block:: python

    from myapp import model
    log.info("Creating tables") 
    model._Base.metadata.drop_all(bind=meta.engine, checkfirst=True)
    model._Base.metadata.create_all(bind=meta.engine) 
    log.info("Successfully setup") 


Then run the following on the command line: 

.. code-block:: bash

    paster setup-app development.ini 


Data queries and modifications
------------------------------


.. important::  
   
   this section assumes you're putting the code in a high-level model function. If you're putting it directly into a controller method, you'll have to put a `model.` prefix in front of every object defined in the model, or import the objects individually. Also note that the `Session` object here (capital s) is not the same as the Beaker `session` object (lowercase s) in controllers. 

Here's how to enter new data into the database: 

.. code-block:: python

    mr_jones = Person() 
    mr_jones.name = 'Mr Jones' 
    meta.Session.save(mr_jones) 
    meta.Session.commit() 


`mr_jones` here is an instance of `Person`. Its properties correspond to the column titles of `t_people` and contain the data from the selected row. A more sophisticated application would have a `Person.\_\_init\_\_` method that automatically sets attributes based on its arguments. 


An example of loading a database entry in a controller method, performing a sex change, and saving it: 

.. code-block:: python

    person_q = meta.Session.query(Person) # An ORM Query object for accessing the Person table 
    mr_jones = person_q.filter(Person.name=='Mr Jones').one() 
    print mr_jones.name # prints 'Mr Jones' 
    mr_jones.name = 'Mrs Jones' # only the object instance is changed here ... 
    meta.Session.commit() # ... only now is the database updated 


To return a list of entries use: 

.. code-block:: python

    all_mr_joneses = person_q.filter(Person.name=='Mr Jones').all() 


To get all list of all the people in the table use: 

.. code-block:: python

    everyone = person_q.all() 


To retrieve by id: 

.. code-block:: python

    someuser = person_q.get(5) 


You can iterate over every person even more simply: 

.. code-block:: python

    print "All people" 
    for p in person_q: 
        print p.name 
    print 
    print "All Mr Joneses:" 
    for p in person_q.filter(Person.name=='Mr Jones'): 
        print p.name 


To delete an entry use the following: 

.. code-block:: python

    mr_jones = person_q.filter(Person.name=='Mr Jones').one() 
    meta.Session.delete(mr_jones) 
    meta.Session.commit() 


Working with joined objects 
^^^^^^^^^^^^^^^^^^^^^^^^^^^


Recall that the `my_addresses` property is a list of `Address` objects 

.. code-block:: python

    print mr_jones.my_addresses[0].address # prints first address 


To add an existing address to 'Mr Jones' we do the following: 

.. code-block:: python

    address_q = meta.Session.query(Address) 
    
    # Retrieve an existing address 
    address = address_q.filter(Address.address=='33 Pine Marten Lane, Pleasantville').one()
    
    # Add to the list 
    mr_jones.my_addresses.append(new_address)
    
    # issue updates to the join table
    meta.Session.commit()  


To add an entirely new address to 'Mr Jones' we do the following: 

.. code-block:: python

    new_address = Address() # Construct an empty address object 
    new_address.address = '33 Pine Marten Lane, Pleasantville' 
    mr_jones.my_addresses.append(new_address) # Add to the list 
    meta.Session.commit() # Commit changes to the database 


After making changes you must call `meta.Session.commit()` to store them permanently in the database; otherwise they'll be discarded at the end of the web request. You can also call `meta.Session.rollback()` at any time to undo any changes that haven't been committed. 

To search on a joined object we can pass an entire object as a query: 

.. code-block:: python

    search_address = Address() 
    search_address.address = '33 Pine Marten Lane, Pleasantville' 
    residents_at_33_pine_marten_lane = \
        person_q.filter(Person.my_addresses.contains(search_address)).all() 


All attributes must match in the query object. 

Or we can search on a joined objects' property, 

.. code-block:: python

    residents_at_33_pine_marten_lane = \
     person_q.join('my_addresses').filter(
        Address.address=='33 Pine Marten Lane, Pleasantville').all() 


A shortcut for the above is to use `any()`:

.. code-block:: python

    residents_at_33_pine_marten_lane = \
     person_q.filter(Person.my_addresses.any(
        Address.address=='33 Pine Marten Lane, Pleasantville')).all() 



To disassociate an address from Mr Jones we do the following: 

.. code-block:: python

    del mr_jones.my_addresses[0] # Delete the reference to the address 
    meta.Session.commit() 


To delete the address itself in the address table, normally we'd have to issue a separate `delete()` for the `Address` object itself: 

.. code-block:: python

    meta.Session.delete(mr_jones.my_addresses[0]) # Delete the Address object 
    del mr_jones.my_addresses[0] 
    meta.Session.commit() # Commit both operations to the database 


However, SQLAlchemy supports a shortcut for the above operation. Configure the mapper relation using `cascade = "all, delete-orphan"` instead: 

.. code-block:: python

    orm.mapper(Address, t_addresses) 
    orm.mapper(Person, t_people, properties = { 
    'my_addresses' : orm.relation(
            Address, secondary=t_addresses_people, cascade="all,delete-orphan"), 
    }) 


Then, any items removed from `mr_jones.my_addresses` is automatically deleted from the database: 


.. code-block:: python

    del mr_jones.my_addresses[0] # Delete the reference to the address, 
                                 # also deletes the Address 
    meta.Session.commit() 


For any relationship, you can add `cascade = "all, delete-orphan"` as an extra argument to `relation()` in your mappers to ensure that when a join is deleted the joined object is deleted as well, so that the above delete() operation is not needed - only the removal from the `my_addresses` list. Beware though that despite its name, `delete-orphan` removes joined objects even if another object is joined to it. 

Non-ORM SQL queries 
^^^^^^^^^^^^^^^^^^^


Use `meta.Session.execute()` to execute a non-ORM SQL query within the session's transaction. Bulk updates and deletes can modify records significantly faster than looping through a query and modifying the ORM instances. 

.. code-block:: python

    q = sa.select([table1.c.id, table1.c.name], order_by=[table1.c.name]) 
    records = meta.Session.execute(q).fetchall() 

    # Example of a bulk SQL UPDATE. 
    update = table1.update(table1.c.name=="Jack") 
    meta.Session.execute(update, name="Ed") 
    meta.Session.commit() 

    # Example of updating all matching records using an expression. 
    update = table1.update(values={table1.c.entry_id: table1.c.entry_id + 1000}) 
    meta.Session.exececute(update) 
    meta.Session.commit() 

    # Example of a bulk SQL DELETE. 
    delete = table1.delete(table1.c.name.like("M%")) 
    meta.Session.execute(delete) 
    meta.Session.commit() 

    # Database specific, use only if SQLAlchemy doesn't have methods to construct the desired query. 
    meta.Session.execute("ALTER TABLE Foo ADD new_column (VARCHAR(255)) NOT NULL") 


.. warning:: The last example changes the database structure and may adversely interact with ORM operations. 


Further reading 
^^^^^^^^^^^^^^^


The Query object has many other features, including filtering on conditions, ordering the results, grouping, etc. These are excellently described in the SQLAlchemy manual. See especially the `Data Mapping <http://www.sqlalchemy.org/docs/datamapping.html>`_ and `Session / Unit of Work <http://www.sqlalchemy.org/docs/unitofwork.html>`_ chapters. 

Testing Your Models
-------------------


Normal model usage works fine in model tests, however to use the metadata you must specify an engine connection for it. To have your tables created for every unit test in your project, use a test_models.py such as: 

.. code-block:: python

    from myapp.tests import * 
    from myapp import model 
    from myapp.model import meta 

    class TestModels(TestController): 
        def setUp(self): 
            meta.Session.remove() 
            meta.metadata.create_all(meta.engine) 

        def test_index(self): 
            # test your models 


.. note:: Notice that the tests inherit from TestController. This is to ensure that the application is setup so that the models will work. 


"nosetests --with-pylons=/path/to/test.ini ..." is another way to ensure that your model is properly initialized before the tests are run. This can be used when running non-controller tests. 

Multiple engines
----------------


Some applications need to connect to multiple databases (engines). Some always bind certain tables to the same engines (e.g., a general database and a logging database); this is called "horizontal partitioning". Other applications have several databases with the same structure, and choose one or another depending on the current request. A blogging app with a separate database for each blog, for instance. A few large applications store different records from the same logical table in different databases to prevent the database size from getting too large; this is called "vertical partitioning" or "sharding". The pattern above can accommodate any of these schemes with a few minor changes. 

First, you can define multiple engines in your config file like this: 

.. code-block:: ini

    sqlalchemy.default.url = "mysql://..." 
    sqlalchemy.default.pool_recycle = 3600 
    sqlalchemy.log.url = "sqlite://..." 

This defines two engines, "default" and "log", each with its own set of options. Now you have to instantiate every engine you want to use. 

.. code-block:: python

    default_engine = engine_from_config(config, 'sqlalchemy.default.') 
    log_engine = engine_from_config(config, 'sqlalchemy.log.') 
    init_model(default_engine, log_engine) 


Of course you'll have to modify `init_model()` to accept both arguments and create two engines. 

To bind different tables to different databases, but always with a particular table going to the same engine, use the `binds` argument to `sessionmaker` rather than `bind`: 

.. code-block:: python

    binds={"table1": engine1, "table2": engine2} 
    Session = scoped_session(sessionmaker(
                    transactional=True, autoflush=True, binds=binds) 


To choose the bindings on a per-request basis, skip the sessionmaker bind(s) argument, and instead put this in your base controller's `\_\_call\_\_` method before the superclass call, or directly in a specific action method: 

.. code-block:: python

    meta.Session.configure(bind=meta.engine) 


`binds=` works the same way here too. 

Discussion on coding style, the Session object, and bound metadata
------------------------------------------------------------------


All ORM operations require a `Session` and an engine. All non-ORM SQL operations require an engine. (Strictly speaking, they can use a connection instead, but that's beyond the scope of this tutorial.) You can either pass the engine as the `bind=` argument to every SQLAlchemy method that does an actual database query, or bind the engine to a session or metadata. This tutorial recommends binding the session because that is the most flexible, as shown in the "Multiple Engines" section above. 

It's also possible to bind a metadata to an engine using the `MetaData(engine)` syntax, or to change its binding with `metadata.bind = engine`. This would allow you to do autoloading without the `autoload_with` argument, and certain SQL operations without specifying an engine or session. Bound metadata was common in earlier versions of SQLAlchemy but is no longer recommended for beginners because it can cause unexpected behavior when ORM and non-ORM operations are mixed. 

Don't confuse SQLAlchemy sessions and Pylons sessions; they're two different things! The `session` object used in controllers (`pylons.session`) is an industry standard used in web applications to maintain state between web requests by the same user. SQLAlchemy's session is an object that synchronizes ORM objects in memory with their corresponding records in the database. 

The `Session` variable in this chapter is _not_ a SQLAlchemy session object; it's a "contextual session" class. Calling it returns the (new or existing) session object appropriate for this web request, taking into account threading and middleware issues. Calling its class methods (`Session.commit()`, `Session.query(...)`, etc) implicitly calls the corresponding method on the appropriate session. You can normally just call the `Session` class methods and ignore the internal session objects entirely. See "Contextual/Thread-local Sessions" in the SQLAlchemy manual for more information. This is equivalent to SQLAlchemy 0.3's `SessionContext` but with a different API. 

"Transactional" sessions are a new feature in SQLAlchemy 0.4; this is why we're using `Session.commit()` instead of `Session.flush()`. The `transactional` and `autoflush` args to `sessionmaker` enable this, and should normally be used together. 

Fancy classes
-------------


Here's an ORM class with some extra features: 

.. code-block:: python

    class Person(object): 
        def __init__(self, firstname, lastname, sex): 
            if not firstname: raise ValueError("arg 'firstname' cannot be blank") 
            if not lastname: raise ValueError("arg 'lastname' cannot be blank") 
            if sex not in ["M", "F"]: raise ValueError("sex must be 'M' or 'F'") 
            self.firstname = firstname 
            self.lastname = lastname 
            self.sex = sex 

        def __repr__(self): 
            myclass = self.__class__.__name__ 
            return "<%s %s %s>" % (myclass, self.firstname, self.lastname) 
            #return "%s(%r, %r)" % (myclass, self.firstname, self.lastname, self.sex) 
            #return "<%s %s>" % (self.firstname, self.lastname) 

        @property 
        def name(self): 
            return "%s %s" % (self.firstname, self.lastname) 

        @classmethod 
        def all(class_, order=None, sex=None): 
            """Return a Query of all Persons. The caller can iterate this,
            do q.count(), add additional conditions, etc. 
            """ 
            q = meta.Session.query(Person) 
            if order and order.lower().startswith("d"): 
                q = q.order_by([Person.birthdate.desc()]) 
            else: 
                q = q.order_by([Person.lastname, Person.firstname]) 
            return q 

        @classmethod 
        def recent(self, cutoff_days=30): 
            cutoff = datetime.date.today() - datetime.timedelta(days=cutoff_days) 
            q = meta.Session.query(Person).order_by(
                    [Person.last_transaction_date.desc()]) 
            q = q.filter(Person.last_transaction_date >= cutoff) 
            return q 


With this class you can create new records with constructor args. This is not only convenient but ensures the record starts off with valid data (no required field empty). `.\_\_init\_\_` is not called when loading an existing record from the database, so it doesn't interfere with that. Instances can print themselves in a friendly way, and a read-only property is calculated from multiple fields. 

Class methods return high-level queries for the controllers. If you don't like the class methods you can have a separate `PersonSearch` class for them. The methods get the session from the `myapp.model.meta` module where we've stored it. Note that this module imported the `meta` module, not the `Session` object directly. That's because `init_model()` replaces the `Session` object, so if we'd imported the `Session` object directly we'd get its original value rather than its current value. 

You can do many more things in SQLAlchemy, such as a read-write property on a hidden column, or specify relations or default ordering in the `orm.mapper` call. You can make a composite property like `person.location.latitude` and `person.location.longitude` where `latitude` and `longitude` come from different table columns. You can have a class that mimics a list or dict but is associated with a certain table. Some of these properties you'll make with Pylons normal property mechanism; others you'll do with the `property` argument to `orm.mapper`. And you can have relations up the gazoo, which can be lazily loaded if you don't use one side of the relation much of the time, or eagerly loaded to minimize the number of queries. (Only the latter use SQL joins.) You can have certain columns in your class lazily loaded too, although SQLAlchemy calls this "deferred" rather than "lazy". SQLAlchemy will automatically load the columns or related table when they're accessed. 

If you have any more clever ideas for fancy classes, please add a comment to this article. 

Logging
-------


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

SQLAlchemy has several other loggers you can configure in the same way. "sqlalchemy.pool" level INFO tells when connections are checked out from the engine's connection pool and when they're returned. "sqlalchemy.orm" and buddies log various ORM operations. See "Configuring Logging" in the SQLAlchemy manual. 

Multiple application instances
------------------------------


If you're running multiple instances of the _same_ Pylons application in the same WSGI process (e.g., with Paste HTTPServer's "composite" application), you may run into concurrency issues. The problem is that :class:`Session` is thread local but not application-instance local. We're not sure how much this is really an issue if ``Session.remove()`` is properly called in the base controller, but just in case it becomes an issue, here are possible remedies: 

1) Attach the engine(s) to ``pylons.g`` (aka. ``config["pylons.g"]``) rather than to the `meta` module. The globals object is not shared between application instances. 

2) Add a scoping function. This prevents the application instances from sharing the same session objects. Add the following function to your model, and pass it as the second argument to `scoped_session`: 

.. code-block:: python

    def pylons_scope(): 
        import thread 
        from pylons import config 
        return "Pylons|%s|%s" % (thread.get_ident(), config._current_obj()) 

    Session = scoped_session(sessionmaker(...), pylons_scope) 


If you're affected by this, or think you might be, please bring it up on the pylons-discuss mailing list. We need feedback from actual users in this situation to verify that our advice is correct. 

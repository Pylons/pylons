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

The recommend and most common approach used in Pylons applications is to use SQLAlchemy with the declarative configuration style and develop with a relational database (Postgres, MySQL, etc). 

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

When creating a Pylons project, one of the questions asked is whether the project should be configured with SQLAlchemy. Before continuing, ensure that the project was created with this option, if its missing the :file:`model/meta.py` file, then the project should be re-created with this option.
    
.. tip::
    
    The project doesn't need to be deleted to add this option, just re-run
    the `paster` command in the projects parent directory and answer yes
    to the SQLAlchemy prompt. The files will then be added, and existing
    files will present a prompt on whether to replace them or leave the
    current file.


Configure SQLAlchemy
--------------------

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

Don't be tempted to use the ".echo" option to enable SQL logging because it may cause duplicate log output. Instead see the `Logging`_ section below to integrate MySQL logging into Paste's logging system. 


For PostgreSQL 
^^^^^^^^^^^^^^

.. code-block:: ini

    sqlalchemy.url = postgres://username:password@host:port/database 


Enter your username, password, host (localhost if it is on your machine), port number (usually 5432) and the name of your database. 


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
required by SQLAlchemy (:class:`Session`, ``metadata``, and ``engine``) to 
avoid import issues. The objects are optional in the context of other applications that do not make use of them and so if you answer "no" to the SQLAlchemy question when creating a Pylons project, the creation of :file:`model/meta.py` is simply skipped.

It's recommended that for each model, a new module inside the ``model/``
directory should be created. This keeps the models tidy when they get larger as more domain specific code is added to each one.


Creating a Model
================

SQLAlchemy 0.5 has an optional Declarative syntax which offers the 
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

Here's an example of a `Person` and an `Address` class with a one-to-many relationship on `person.addresses`.

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

Diving into SQLAlchemy
======================

SQLAlchemy's SQL Layer
----------------------

SQLAlchemy's lower level SQL expressions can be used along with your ORM
models, and organizing them as class methods can be an effective way to keep
the domain logic separate, and write efficient queries that return subsets
of data that don't map cleanly to the ORM.

Consider the case that you want to get all the unique addresses from the
relation example above. The following method in the Address class can make
it easy:

.. code-block:: python
    
    # Additional imports
    from sqlalchemy import select, func
    
    from myapp.model.meta import Session
    
    
    class Address(object):
        @classmethod
        def unique_addresses(cls):
            """Query the db for distinct addresses, return them as a list"""
            query = select([func.distinct(t_addresses.c.address).label('address')],
                           from_obj=[t_addresses])
            return [row['address'] for row in Session.execute(query).fetchall()]

.. seealso::
    
    SQLAlchemy's `SQL Expression Language Tutorial <http://www.sqlalchemy.org/docs/05/sqlexpression.html>`_


Data queries and modifications
------------------------------

.. important::  
   
   this section assumes you're putting the code in a high-level model function. If you're putting it directly into a controller method, you'll have to put a `model.` prefix in front of every object defined in the model, or import the objects individually. Also note that the `Session` object here (capital s) is not the same as the Beaker `session` object (lowercase s) in controllers. 

Here's how to enter new data into the database: 

.. code-block:: python

    mr_jones = Person() 
    mr_jones.name = 'Mr Jones' 
    meta.Session.add(mr_jones) 
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
    'my_addresses': orm.relation(
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

The Query object has many other features, including filtering on conditions, ordering the results, grouping, etc. These are excellently described in the `SQLAlchemy manual`_. See especially the `Data Mapping <http://www.sqlalchemy.org/docs/datamapping.html>`_ and `Session / Unit of Work <http://www.sqlalchemy.org/docs/unitofwork.html>`_ chapters. 

Testing the Models
==================

Normal model usage works fine in model tests, however to use the metadata you must specify an engine connection for it. To have your tables created for every unit test in your project, use a test_models.py such as: 

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


Coding style, the Session object, and bound metadata
====================================================

All ORM operations require a `Session` and an engine. All non-ORM SQL operations require an engine. (Strictly speaking, they can use a connection instead, but that's beyond the scope of this tutorial.) You can either pass the engine as the `bind=` argument to every SQLAlchemy method that does an actual database query, or bind the engine to a session or metadata. This tutorial recommends binding the session because that is the most flexible, as shown in the :ref:`multiple_databases` section. 

It's also possible to bind a metadata to an engine using the `MetaData(engine)` syntax, or to change its binding with `metadata.bind = engine`. This would allow you to do autoloading without the `autoload_with` argument, and certain SQL operations without specifying an engine or session. Bound metadata was common in earlier versions of SQLAlchemy but is no longer recommended for beginners because it can cause unexpected behavior when ORM and non-ORM operations are mixed. 

Don't confuse SQLAlchemy sessions and Pylons sessions; they're two different things! The `session` object used in controllers (`pylons.session`) is an industry standard used in web applications to maintain state between web requests by the same user. SQLAlchemy's session is an object that synchronizes ORM objects in memory with their corresponding records in the database. 

The `Session` variable in this chapter is _not_ a SQLAlchemy session object; it's a "contextual session" class. Calling it returns the (new or existing) session object appropriate for this web request, taking into account threading and middleware issues. Calling its class methods (`Session.commit()`, `Session.query(...)`, etc) implicitly calls the corresponding method on the appropriate session. You can normally just call the `Session` class methods and ignore the internal session objects entirely. See "Contextual/Thread-local Sessions" in the `SQLAlchemy manual`_ for more information. This is equivalent to SQLAlchemy 0.3's `SessionContext` but with a different API. 

"Transactional" sessions are a new feature in SQLAlchemy 0.4; this is why we're using `Session.commit()` instead of `Session.flush()`. The `autocommit=False` (`transactional=True` in SQLALchemy 0.4) and `autoflush=True` args (which are the defaults) to `sessionmaker` enable this, and should normally be used together. 

Fancy classes
-------------

Here's an ORM class with some extra features: 

.. code-block:: python

    class Person(object): 

        def __init__(self, firstname, lastname, sex): 
            if not firstname:
                raise ValueError("arg 'firstname' cannot be blank") 
            if not lastname:
                raise ValueError("arg 'lastname' cannot be blank") 
            if sex not in ["M", "F"]:
                raise ValueError("sex must be 'M' or 'F'") 
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
        def all(cls, order=None, sex=None): 
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

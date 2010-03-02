.. _advanced_models:

===============
Advanced Models
===============

Pylons works well with many different types of databases, in addition to other database object-relational mappers.

Advanced SQLAlchemy
===================

Alternative SQLAlchemy Styles
-----------------------------

In addition to the declarative style, SQLAlchemy has a default more verbose and explicit approach.

Definitions using the default SQLAlchemy approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample :file:`model/__init__.py` with a "persons" table, based on 
the default SQLAlchemy approach:

.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from sqlalchemy import orm

    from myapp.model import meta

    def init_model(engine):
        meta.Session.configure(bind=engine)
        meta.engine = engine


    t_persons = sa.Table("persons", meta.metadata,
        sa.Column("id", sa.types.Integer, primary_key=True),
        sa.Column("name", sa.types.String(100), primary_key=True),
        sa.Column("email", sa.types.String(100)),
        )

    class Person(object):
        pass

    orm.mapper(Person, t_persons)

This model has one table, "persons", assigned to the variable ``t_persons``.
:class:`Person` is an ORM class which is bound to the table via the mapper.

Relation example 
++++++++++++++++

Here's an example of a `Person` and an `Address` class with a many:many relationship on `people.my_addresses`. See `Relational Databases for People in a Hurry <http://wiki.pylonshq.com/display/pylonscookbook/Relational+databases+for+people+in+a+hurry>`_ and the `SQLAlchemy manual`_ for details. 

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


Definitions using "reflection" of an existing database table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the table already exists, SQLAlchemy can read the column definitions 
directly from the database. This is called *reflecting* the table.

The advantage of this approach is that it allows you to dispense with the 
task of specifying the column types in Python code.  

Reflecting existing database tables must be done inside :func:`init_model` 
because to perform the reflection, a live database engine is required and this 
is not available when the module is imported. A live database engine is bound 
explicitly in the :func:`init_model` function and so enables reflection. 

(An *engine* is a SQLAlchemy object that knows how to connect to a particular
database.)  

Here's the second example with reflection:

.. code-block:: python

    """The application's model objects"""
    import sqlalchemy as sa
    from sqlalchemy import orm

    from myapp.model import meta

    def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        # Reflected tables must be defined and mapped here
        global t_persons
        t_persons = sa.Table("persons", meta.metadata, autoload=True,
                             autoload_with=engine)
        orm.mapper(Person, t_persons)

        meta.Session.configure(bind=engine)
        meta.engine = engine


    t_persons = None

    class Person(object):
        pass

Note how ``t_persons`` and the :func:`orm.mapper` call moved into 
:func:`init_model`, while the ``Person`` class didn't have to.  Also note 
the ``global t_persons`` statement.  This tells Python that ``t_persons`` 
is a global variable outside the function.  ``global`` is required when 
assigning to a global variable inside a function.  It's not required if 
you're merely modifying a mutable object in place, which is why ``meta`` 
doesn't have to be declared global.

Using the model standalone 
^^^^^^^^^^^^^^^^^^^^^^^^^^

You now have everything necessary to use the model in a standalone script such as a cron job, or to test it interactively. You just need to create a SQLAlchemy engine and connect it to the model. This example uses a database "test.sqlite" in the current directory: 

.. code-block:: pycon

    % python 
    Python 2.5.1 (r251:54863, Oct 5 2007, 13:36:32) 
    [GCC 4.1.3 20070929 (prerelease) (Ubuntu 4.1.2-16ubuntu2)] on linux2 
    Type "help", "copyright", "credits" or "license" for more information. 
    >>> import sqlalchemy as sa 
    >>> engine = sa.create_engine("sqlite:///test.sqlite") 
    >>> from myapp import model 
    >>> model.init_model(engine) 

Now you can use the tables, classes, and Session as described in the
`SQLAlchemy manual`_.  For example:

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
    meta.Session.add(a)

    b = model.Person()
    b.name = "Bbb"
    b.email = "bbb@example.com"
    meta.Session.add(b)

    meta.Session.commit()

    # Display all records in the persons table.
    print "Database data:"
    for p in meta.Session.query(model.Person):
        print "id:", p.id
        print "name:", p.name
        print "email:", p.email
        print

.. _multiple_databases:

Talking to Multiple Databases at Once
-------------------------------------

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

    binds = {"table1": engine1, "table2": engine2} 
    Session = scoped_session(sessionmaker(binds=binds))


To choose the bindings on a per-request basis, skip the sessionmaker bind(s) argument, and instead put this in your base controller's `\_\_call\_\_` method before the superclass call, or directly in a specific action method: 

.. code-block:: python

    meta.Session.configure(bind=meta.engine) 


`binds=` works the same way here too. 

Multiple Application Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're running multiple instances of the _same_ Pylons application in the same WSGI process (e.g., with Paste HTTPServer's "composite" application), you may run into concurrency issues. The problem is that :class:`Session` is thread local but not application-instance local. We're not sure how much this is really an issue if ``Session.remove()`` is properly called in the base controller, but just in case it becomes an issue, here are possible remedies: 

1) Attach the engine(s) to ``pylons.g`` (aka. ``config["pylons.g"]``) rather than to the `meta` module. The globals object is not shared between application instances. 

2) Add a scoping function. This prevents the application instances from sharing the same session objects. Add the following function to your model, and pass it as the second argument to `scoped_session`: 

.. code-block:: python

    def pylons_scope(): 
        import thread 
        from pylons import config 
        return "Pylons|%s|%s" % (thread.get_ident(), config._current_obj()) 

    Session = scoped_session(sessionmaker(), pylons_scope) 


If you're affected by this, or think you might be, please bring it up on the pylons-discuss mailing list. We need feedback from actual users in this situation to verify that our advice is correct. 


Non-SQLAlchemy libraries
========================

Most of these expose only the object-relational mapper; their SQL builder and connection pool are not meant to be used directly.

`Storm <http://storm.canonical.com>`_

`Geniusql <http://www.aminus.net/geniusql>`_

DB-API
------

All the SQL libraries above are built on top of Python's DB-API, which provides a common low-level interface for interacting with several database engines: MySQL, PostgreSQL, SQLite, Oracle, Firebird, MS-SQL, Access via ODBC, etc.  Most programmers do not use DB-API directly because its API is low-level and repetitive and does not provide a connection pool.  There's no "DB-API package" to install because it's an abstract interface rather than software.  Instead, install the Python package for the particular engine you're interested in.  Python's `Database Topic Guide <http://www.python.org/topics/database/>`_ describes the DB-API and lists the package required for each engine.  The `sqlite3 <http://docs.python.org/lib/module-sqlite3.html>`_ package for SQLite is included in Python 2.5.

Object Databases
================

Object databases store Python dicts, lists, and classes in pickles, allowing you to access hierarchical data using normal Python statements rather than having to map them to tables, relations, and a foreign language (SQL).

`ZODB <http://wiki.zope.org/ZODB/FrontPage>`_

`Durus <http://www.mems-exchange.org/software/durus/>`_ [#]_

.. [#] Durus is not thread safe, so you should use its server mode if your
   application writes to the database.  Do not share connections between
   threads.  ZODB is thread safe, so it may be a more convenient alternative.

Popular No-SQL Databases
========================

Pylons can also work with other database systems, such as the following:

`Schevo <http://schevo.org/>`_ uses Durus to combine some features of relational and object databases.  It is written in Python.

`CouchDb <http://couchdb.org/>`_ is a document-based database.  It features a `Python API <http://code.google.com/p/couchdb-python/>`_.

The Datastore database in Google App Engine.

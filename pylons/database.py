"""Provides convenient access to SQLObject-managed and/or SQLAlchemy-managed
databases.

This module enables easy use of an SQLObject database by providing an 
auto-connect hub that will utilize the db uri string given in the Paste conf
file called ``sqlobject.dburi``.

A SQLAlchemy ``SessionContext`` is also available: it provides both thread and
process safe ``Session`` objects via the ``session_context.current`` property.
"""
import thread

from paste.deploy.converters import asbool

import pylons
import pylons.util

__all__ = ["PackageHub", "AutoConnectHub"]

# Provide support for sqlalchemy
_db_engines = {}
try:
    import sqlalchemy
    from sqlalchemy.ext import sessioncontext

    def app_scope():
        """Return the id keying the current database session's scope.

        The session is particular to the current Pylons application -- this
        returns an id generated from the current thread and the current Pylons
        application's Globals object at pylons.g (if one is registered).
        """
        try:
            app_scope_id = str(id(pylons.g._current_obj()))
        except TypeError:
            app_scope_id = ''
        return '%s|%i' % (app_scope_id, thread.get_ident())

    def create_engine(uri=None, echo=None, **kwargs):
        """Return a SQLAlchemy db engine. Uses the configuration values from
        ``get_engine_conf`` for uri and echo if none are specified.

        Engines are cached in the ``get_engines`` dict.
        """
        uri, echo = get_engine_conf(uri, echo)
        kwargs['echo'] = echo
        engine_key = '%s|%s' % (uri, str(kwargs))
        db_engines = get_engines()
        if engine_key in db_engines:
            engine = db_engines[engine_key]
        else:
            engine = db_engines[engine_key] = \
                sqlalchemy.create_engine(uri, **kwargs)
        return engine

    def get_engine_conf(uri=None, echo=None):
        """Returns a tuple of SQLAlchemy engine configuration values (uri,
        echo) from the Pylons config file values ``sqlalchemy.dburi`` and
        ``sqlalchemy.echo`` when none are specified."""
        if uri is None:
            uri = pylons.util.config_get('sqlalchemy.dburi')
        if not uri:
            raise KeyError('No SQLAlchemy database config found!')
        if echo is None:
            echo = pylons.util.config_get('sqlalchemy.echo', False)
            if echo != 'debug':
                echo = asbool(echo)
        return uri, echo

    def get_engines():
        """Return a dict of cached SQLAlchemy engines.

        Engines are cached to an application's ``Globals`` (``g``) object. If
        for whatever reason the ``g`` object has not been registered (outside
        of a web request), engines are cached to the global ``engines`` dict
        instead."""
        try:
            if not hasattr(pylons.g, '_db_engines'):
                db_engines = pylons.g._db_engines = {}
            else:
                db_engines = pylons.g._db_engines
            return db_engines
        except TypeError:
            return _db_engines

    def make_session(uri=None, echo=None, session_kwargs=None, **kwargs):
        """Returns a SQLAlchemy session for the specified database uri from
        the the engine cache (returned from ``get_engines``)``. Uses the
        configuration values from ``get_engine_conf`` for uri and echo when
        None are specified.

        ``session_kwargs`` are passed to SQLAlchemy's ``create_session``
        function as keyword arguments.
        
        If the uri's engine does not exist, it will be created and added to
        the engine cache.
        """
        if session_kwargs is None:
            session_kwargs = {}
        engine = create_engine(uri, echo=echo, **kwargs)
        return sqlalchemy.create_session(bind_to=engine, **session_kwargs)

    session_context = sessioncontext.SessionContext(make_session,
                                                    scopefunc=app_scope)

    __all__.extend(['app_scope', 'create_engine', 'get_engine_conf',
                    'make_session', 'session_context'])

except ImportError:
    pass

# Provide support for sqlobject
try:
    import sqlobject
    from sqlobject.dbconnection import ConnectionHub, Transaction, TheURIOpener
except:
    ConnectionHub = object

class AutoConnectHub(ConnectionHub):
    """Connects to the database once per thread.
    
    The AutoConnectHub also provides convenient methods for managing
    transactions.
    """
    uri = None
    params = {}
    
    def __init__(self, uri=None, pool_connections=True):
        if not uri:
            uri = pylons.util.config_get('sqlobject.dburi')
        self.uri = uri
        self.pool_connections = pool_connections
        ConnectionHub.__init__(self)
    
    def getConnection(self):
        try:
            conn = self.threadingLocal.connection
            return conn
        except AttributeError:
            if self.uri:
                conn = sqlobject.connectionForURI(self.uri)
                # the following line effectively turns off the DBAPI connection
                # cache. We're already holding on to a connection per thread,
                # and the cache causes problems with sqlite.
                if self.uri.startswith("sqlite"):
                    TheURIOpener.cachedURIs = {}
                self.threadingLocal.connection = conn
                if not self.pool_connections:
                    # This disables pooling
                    conn._pool = None
                return conn
            try:
                return self.processConnection
            except AttributeError:
                raise AttributeError(
                    "No connection has been defined for this thread "
                    "or process")
    
    def begin(self):
        """Starts a transaction."""
        conn = self.getConnection()
        if isinstance(conn, Transaction):
            if conn._obsolete:
                conn.begin()
            return
        self.threadingLocal.old_conn = conn
        self.threadingLocal.connection = conn.transaction()
        
    def commit(self):
        """Commits the current transaction."""
        conn = self.threadingLocal.connection
        if isinstance(conn, Transaction):
            self.threadingLocal.connection.commit()
    
    def rollback(self):
        """Rolls back the current transaction."""
        conn = self.threadingLocal.connection
        if isinstance(conn, Transaction) and not conn._obsolete:
            self.threadingLocal.connection.rollback()
            
    def end(self):
        """Ends the transaction, returning to a standard connection."""
        conn = self.threadingLocal.connection
        if not isinstance(conn, Transaction):
            return
        if not conn._obsolete:
            conn.rollback()
        self.threadingLocal.connection = self.threadingLocal.old_conn
        del self.threadingLocal.old_conn
        self.threadingLocal.connection.cache.clear()

# This dictionary stores the AutoConnectHubs used for each
# connection URI
_hubs = dict()

class UnconfiguredConnectionError(KeyError):
    """
    Raised when no configuration is available to set up a connection.
    """

class PackageHub(object):
    """Transparently proxies to an AutoConnectHub for the URI
    that is appropriate for this package. A package URI is
    configured via "packagename.dburi" in the Paste ini file
    settings. If there is no package DB URI configured, the
    default (provided by "sqlobject.dburi") is used.
    
    The hub is not instantiated until an attempt is made to
    use the database.

    If pool_connections=False, then a new database connection
    will be opened for every request.  This will avoid
    problems with database connections that periodically die.
    """
    def __init__(self, packagename, dburi=None, pool_connections=True):
        self.packagename = packagename
        self.hub = None
        self.dburi = dburi
        self.pool_connections = pool_connections
    
    def __get__(self, obj, type):
        if not self.hub:
            try:
                self.set_hub()
            except UnconfiguredConnectionError, e:
                raise AttributeError(str(e))
        return self.hub.__get__(obj, type)
    
    def __set__(self, obj, type):
        if not self.hub:
            self.set_hub()
        return self.hub.__set__(obj, type)
    
    def __getattr__(self, name):
        if not self.hub:
            self.set_hub()
        return getattr(self.hub, name)
    
    def set_hub(self):
        dburi = self.dburi
        if not dburi:
            try:
                dburi = pylons.util.config_get("%s.dburi" % \
                                                   self.packagename)
            except TypeError, e:
                # No configuration is registered
                raise UnconfiguredConnectionError(str(e))
        if not dburi:
            dburi = pylons.util.config_get("sqlobject.dburi")
        if not dburi:
            raise UnconfiguredConnectionError(
                "No database configuration found!")
        hub = _hubs.get(dburi)
        if not hub:
            hub = AutoConnectHub(
                dburi, pool_connections=self.pool_connections)
            _hubs[dburi] = hub
        self.hub = hub

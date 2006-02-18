"""Provides convenient access to an SQLObject-managed database.

This module enables easy use of an SQLObject database by providing an auto-connect
hub that will utilize the db uri string given in the Paste conf file called
``sqlobject.dburi``

It is based heavily (if not 99%) on the TurboGears file of the same name.
"""

import sqlobject
from sqlobject.dbconnection import ConnectionHub, Transaction, TheURIOpener
from paste.deploy.config import CONFIG

class AutoConnectHub(ConnectionHub):
    """Connects to the database once per thread.
    
    The AutoConnectHub also provides convenient methods for managing transactions.
    """
    uri = None
    params = {}
    
    def __init__(self, uri=None):
        if not uri:
            uri = CONFIG.current_conf()['app'].get('sqlobject.dburi')
        self.uri = uri
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
                return conn
            try:
                return self.processConnection
            except AttributeError:
                raise AttributeError(
                    "No connection has been defined for this thread "
                    "or process")

    def reset(self):
        """Used for testing purposes. This drops all of the connections
        that are being held."""
        self.threadingLocal = threading_local()
        
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

class PackageHub(object):
    """Transparently proxies to an AutoConnectHub for the URI
    that is appropriate for this package. A package URI is
    configured via "packagename.dburi" in the global CherryPy
    settings. If there is no package DB URI configured, the
    default (provided by "sqlobject.dburi") is used.
    
    The hub is not instantiated until an attempt is made to
    use the database.
    """
    def __init__(self, packagename, dburi=None):
        self.packagename = packagename
        self.hub = None
        self.dburi = dburi
    
    def __get__(self, obj, type):
        if not self.hub:
            self.set_hub()
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
            dburi = CONFIG.current_conf()['app'].get("%s.dburi" % self.packagename, None)
            if not dburi:
                dburi = CONFIG.current_conf()['app'].get("sqlobject.dburi", None)
        if not dburi:
            raise KeyError, "No database configuration found!"
        hub = _hubs.get(dburi, None)
        if not hub:
            hub = AutoConnectHub(dburi)
            _hubs[dburi] = hub
        self.hub = hub
            
__all__ = ["PackageHub", "AutoConnectHub"]
.. _upgrading:

=========
Upgrading
=========

1.0 -> 1.0.1
============

No changes are necessary, however to take advantage of MarkupSafe's faster
HTML escaping, the default filter in ``environment.py`` that Mako is 
configured with should be changed from::
    
    from webhelpers.html import escape

To::
    from markupsafe import escape

MarkupSafe utilizes a C extension where available for faster escaping which
can help on larger pages with substantial variable substitutions.


0.9.7 -> 1.0
============

Upgrading your project is slightly different depending on which versions you're upgrading from and to. It's recommended that upgrades be done in minor revision steps, as deprecation warnings are added between revisions to help in the upgrade process.

For any project prior to 0.9.7, you should first follow the applicable docs to upgrade to 0.9.7 before proceeding.

To upgrade to 1.0, first upgrade your project to 0.10. This is a Pylons release that is fully backwards-compatible with 0.9.7. However under 0.10 a variety of warnings will be issued about the various things that need to be changed before upgrading to 1.0.

.. tip::
    Since Pylons 0.10 is only out as a beta at this point, upgrade using the
    actual URL, for example:
    
    .. code-block:: bash
        
        $ easy_install -U http://pylonshq.com/download/0.10/Pylons-0.10.tar.gz


Beyond the warnings issued, you should also read the following list and ensure these changes have been applied.

Pylons changes from 0.9.7 to 1.0:

* The config object created in ``environment.py`` is now passed around explicitly. There are also some other minor updates as follows.
    
    Update config/environment.py to initialize and return the config::
    
        # Add to the imports:
        from pylons.configuration import PylonsConfig
    
        # Add under 'def load_environment':
        config = PylonsConfig()
        
        # Replace the make_map / app globals line with
        config['routes.map'] = make_map(config)
        config['pylons.app_globals'] = app_globals.Globals(config)
        
        # Optionally, if removing the CacheMiddleware and using the
        # cache in the new 1.0 style, add under the previous lines:
        import pylons
        pylons.cache._push_object(config['pylons.app_globals'].cache)
        
    
        # Add at the end of the load_environment function:
        return config
    
    Update config/middleware.py to use the returned :term:`config`::
        
        # modify the load_environment call:
        config = load_environment(global_conf, app_conf)
        
        # update the middleware calls
        
        # The Pylons WSGI app
        app = PylonsApp(config=config)

        # Routing/Session/Cache Middleware
        app = RoutesMiddleware(app, config['routes.map'])
        app = SessionMiddleware(app, config)

        # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
        
        # Add right before 'return app':
        app.config = config
    
    .. note::
    
        The CacheMiddleware is no longer setup by default through
        middleware, its now setup under :term:`app_globals` inside its 
        instantiation in :file:`lib/app_globals.py`.
    
    Update config/routing.py to accept the :term:`config`::
        
        # Replace the def line with
        def make_map(config):
    
    Update lib/app_globals.py to accept the :term:`config`::
        
        # Replace the __init__ line with
        def __init__(self, config):
        
        # Optionally, if you decided to remove the CacheMiddleware
        # Add these imports
        from beaker.cache import CacheManager
        from beaker.util import parse_cache_config_options
        
        # and add this line in __init__:
        self.cache = CacheManager(**parse_cache_config_options(config))
    
    Update tests/__init__.py as needed::
        
        from unittest import TestCase

        from paste.deploy import loadapp
        from paste.script.appinstall import SetupCommand
        from pylons import url
        from routes.util import URLGenerator
        from webtest import TestApp

        import pylons.test

        __all__ = ['environ', 'url', 'TestController']

        # Invoke websetup with the current config file
        SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

        environ = {}

        class TestController(TestCase):

            def __init__(self, *args, **kwargs):
                wsgiapp = pylons.test.pylonsapp
                config = wsgiapp.config
                self.app = TestApp(wsgiapp)
                url._push_object(URLGenerator(config['routes.map'], environ))
                TestCase.__init__(self, *args, **kwargs)

    .. note::
        
        Change the use of ``url_for`` in your tests to use 
        :class:`url <routes.util.URLGenerator>`, which is imported from
        :file:`tests/__init__.py` in your unit tests.

    
    Finally, update websetup.py to avoid the duplicate app creation that
    previously could occur during the unit tests::
        
        # Add to the imports
        import pylons.test
        
        # Add under the 'def setup_app':
        
        # Don't reload the app if it was loaded under the testing environment
        if not pylons.test.pylonsapp:
            load_environment(conf.global_conf, conf.local_conf)
        
        
* Change all instances of ``redirect_to(...)`` -> ``redirect(url(...))``
    
    ``redirect_to`` processed arguments in a slightly 'magical' manner in that 
    some of them went to the ``url_for`` while sometimes... not. :func:`~pylons.controllers.util.redirect`
    issues a redirect and nothing more, so to generate a url, the :class:`url <routes.util.URLGenerator>`
    instance should be used (import: ``from pylons import url``).

* Ensure that all use of ``g`` is switched to using the new name, :term:`app_globals`

* Change all instances of ``url_for`` to :class:`url <routes.util.URLGenerator>`. 
    
    Note that ``url`` does not retain the current route memory like
    ``url_for`` did by default. To get a route generated using the 
    current route, call 
    :meth:`url.current <routes.util.URLGenerator.current>`.
    
    For example::
        
        # Rather than url_for() for the current route
        url.current()
    
    :class:`url <routes.util.URLGenerator>` can be imported from ``pylons``.

* Change ``config`` import statement if needed
    
    Previously, the config object could be imported as if it was a module::
        
        import pylons.config
    
    The config object is now an object in :file:`pylons/__init__.py` so the
    import needs to be changed to::
        
        from pylons import config

* Routes is now explicit by default
    
    This won't affect those already using :class:`url <routes.util.URLGenerator>` as it ignores route memory. This change does mean that some routes which relied on a default controller of 'content' and a default action of 'index' will not work.
  
    To restore the old behavior, in :file:`config/routing.py`, set the mapper
    to explicit::
    
        map.explicit = True

* By default, the :term:`tmpl_context` (a.k.a 'c'), is no longer a :class:`~pylons.util.AttribSafeContextObj`. This means accessing attributes that don't exist will raise an :exc:`AttributeError`. 
    
    To use the attribute-safe :term:`tmpl_context`, add this line to the
    :file:`config/environment.py`::
        
        config['pylons.strict_tmpl_context'] = False

.. _upgrading:

=========
Upgrading
=========

Upgrading your project is slightly different depending on which versions you're upgrading from and to. It's recommended that upgrades be done in minor revision steps, as deprecation warnings are added between revisions to help in the upgrade process.

For any project prior to 0.9.7, you should first follow the applicable docs to upgrade to 0.9.7 before proceeding.

To upgrade to 1.0, first upgrade your project to 0.10. This is a Pylons release that is fully backwards-compatible with 0.9.7. However under 0.10 a variety of warnings will be issued about the various things that need to be changed before upgrading to 1.0.

Beyond the warnings issued, you should also read the following list and ensure these changes have been applied.

Pylons changes from 0.9.7 to 1.0:

* The config object created in ``environment.py`` is now passed around explicitly.
    
    Update config/environment.py to initialize and return the config::
    
        # Add to the imports:
        from pylons.configuration import PylonsConfig
    
        # Add under 'def load_environment':
        config = PylonsConfig()
    
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
        
* Change all instances of ``redirect_to(...)`` -> ``redirect(url(...))``
    
    ``redirect_to`` processed arguments in a slightly 'magical' manner in that 
    some of them went to the ``url_for`` while sometimes... not. :func:`~pylons.controllers.util.redirect`
    issues a redirect and nothing more, so to generate a url, the :class:`url <routes.util.URLGenerator>`
    instance should be used (import: ``from pylons import url``).

* Ensure that all use of ``g`` is switched to using the new name, :term:`app_globals`

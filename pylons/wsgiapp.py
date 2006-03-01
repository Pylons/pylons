"""WSGI App Creator

This module is responsible for creating the basic Pylons WSGI application. It's generally
assumed that it will be called by Paste, though any WSGI application server could create
and call the WSGI app as well.
"""
from paste.deploy.config import ConfigMiddleware
from paste.deploy.converters import asbool

from myghty.http import WSGIHandler
import myghty
import pylons.middleware

class PylonsWSGIApp(object):
    def __init__(self, global_conf, myghty_config):
        """Basic Pylons WSGI Application

        This basic WSGI app is provided should a web developer want to
        get access to the most basic Myghty WSGI application that Pylons
        utilizes.
        """
        self.app = WSGIHandler.WSGIHandler(**myghty_config)
        self.global_conf = global_conf
    
    def __call__(self, environ, start_response):
        if asbool(self.global_conf.get('debug', 'true')):
            try:
                return self.app.handle(environ, start_response)
            except myghty.exception.Error, e:
                tback = e.raw_excinfo
                delattr(e, 'raw_excinfo')
                if tback[1]: tback[1].mtrace = e
                raise tback[0], tback[1], tback[2]
        else:
            return self.app.handle(environ, start_response)

def make_app(config):
    app = PylonsWSGIApp(config.global_conf, config.myghty)
    app = ConfigMiddleware(app, {
        'default':config.global_conf,
        'app':config.app_conf,
        'app_conf':config.app_conf,
        'global_conf':config.global_conf
    })
    g = pylons.middleware.Globals()
    try:
        package = __import__(config.package + '.lib.app_globals', globals(), locals(), ['Globals'])
    except ImportError:
        pass
    else:
        g = package.Globals(config.global_conf, config.app_conf, config=config)
    g.pylons_config = config
    app = pylons.middleware.register_app_globals(app, g)
    return app

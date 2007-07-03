from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.registry import RegistryManager
from paste.deploy.config import ConfigMiddleware, CONFIG
from paste.deploy.converters import asbool

from pylons.error import error_template
from pylons import config
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp

import projectname.lib.helpers
import projectname.lib.app_globals as app_globals
from projectname.config.environment import load_environment

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    
    """
    # Load our Pylons configuration defaults
    load_environment(global_conf, app_conf)
    
    # Add the second engine
    kidopts = {'kid.assume_encoding':'utf-8', 'kid.encoding':'utf-8'}
    config.add_template_engine('kid', 'projectname.kidtemplates', kidopts)
        
    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.PylonsApp(helpers=projectname.lib.helpers,
                                   g=app_globals.Globals)
    app = ConfigMiddleware(app, config._current_obj())
    
    # If errror handling and exception catching will be handled by middleware
    # for multiple apps, you will want to set full_stack = False in your config
    # file so that it can catch the problems.
    if asbool(full_stack):
        # Change HTTPExceptions to HTTP responses
        app = httpexceptions.make_middleware(app, global_conf)
    
        # Error Handling
        app = ErrorHandler(app, global_conf, error_template=error_template, **config['pylons.errorware'])
    
        # Display error documents for 401, 403, 404 status codes (if debug is disabled also
        # intercepts 500)
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    
    # Establish the Registry for this application
    app = RegistryManager(app)
    
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    javascripts_app = StaticJavascripts()
    app = Cascade([static_app, javascripts_app, app])
    return app

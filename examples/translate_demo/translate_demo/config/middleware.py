from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool

from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, error_mapper
import pylons.wsgiapp

from translate_demo.config.environment import load_config, paths

def make_app(global_conf, **kw):
    """
    Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    """
    
    # Load our Pylons configuration defaults
    config = load_config(global_conf, **kw)
    global_conf, kw = config['global_conf'], config['kw']
        
    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.make_app(global_conf, config['myghty_config'], package='translate_demo', **kw)
    g = app.globals
    
    # YOUR MIDDLEWARE
    # Put your own middleware here, so that any problems are caught by the error
    # handling middleware underneath
    
    # @@@ Change HTTPExceptions to HTTP responses @@@
    app = httpexceptions.make_middleware(app, global_conf)
    
    # @@@ Error Handling @@@
    app = ErrorHandler(app, global_conf, error_template=error_template, **config['errorware'])
       
    # @@@ Display error documents for 401, 403, 404 status codes (if debug is False also intercepts 500) @@@
    app = ErrorDocuments(app, global_conf, mapper=error_mapper, **kw)
    
    # @@@ Static Files in public directory @@@
    staticapp = StaticURLParser(paths['static_files'])
    
    # @@@ Cascade @@@ 
    app = Cascade([staticapp, app])
    return app
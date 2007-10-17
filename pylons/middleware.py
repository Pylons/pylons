"""Pylons' WSGI middlewares"""
import logging
import os.path
import urllib

from paste.deploy.converters import asbool
from paste.errordocument import StatusBasedForward
from paste.recursive import RecursiveMiddleware
from paste.urlparser import StaticURLParser

from webhelpers.rails.asset_tag import javascript_path

__pudge_all__ = ['StaticJavascripts', 'ErrorHandler', 'ErrorDocuments']

media_path = os.path.join(os.path.dirname(__file__), 'media')

log = logging.getLogger(__name__)


class StaticJavascripts(object):
    """Middleware for intercepting requests for WebHelpers' included 
    javascript files.
    
    Triggered when PATH_INFO begins with '/javascripts/'.
    """
    def __init__(self, **kwargs):
        self.javascripts_app = \
            StaticURLParser(os.path.dirname(javascript_path), **kwargs)
        
    def __call__(self, environ, start_response):
        if environ.get('PATH_INFO', '').startswith('/javascripts/'):
            log.debug("Handling Javascript URL (Starts with /javascripts/)")
            return self.javascripts_app(environ, start_response)
        else:
            return self.javascripts_app.not_found(environ, start_response)


def ErrorHandler(app, global_conf, **errorware):
    """ErrorHandler Toggle
    
    If debug is enabled, this function will return the app wrapped in
    our customized Paste EvalException middleware we have called the
    ``PylonsEvalException``.
    
    Otherwise, the app will be wrapped in the Paste ErrorMiddleware, and
    the ``errorware`` dict will be passed into it.
    """
    if asbool(global_conf.get('debug')):
        from pylons.error import PylonsEvalException
        app = PylonsEvalException(app, global_conf, **errorware)
    else:
        from paste.exceptions.errormiddleware import ErrorMiddleware
        if 'error_template' in errorware:
            del errorware['error_template']
        app = ErrorMiddleware(app, global_conf, **errorware)
    return app


def error_mapper(code, message, environ, global_conf=None, **kw):
    if environ.get('pylons.error_call'):
        return
    else:
        environ['pylons.error_call'] = True
    
    if global_conf is None:
        global_conf = {}
    codes = [401, 403, 404]
    if not asbool(global_conf.get('debug')):
        codes.append(500)
    if code in codes:
        # StatusBasedForward expects a relative URL (no SCRIPT_NAME)
        url = '/error/document/?%s' % (urllib.urlencode({'message': message,
                                                         'code': code}))
        return url


def ErrorDocuments(app, global_conf=None, mapper=None, **kw):
    """Wraps the app in error docs using Paste RecursiveMiddleware and
    ErrorDocumentsMiddleware
    
    All the args are passed directly into the ErrorDocumentsMiddleware. If no
    mapper is given, a default error_mapper is passed in.
    """
    if global_conf is None:
        global_conf = {}
    if mapper is None:
        mapper = error_mapper
    return RecursiveMiddleware(StatusBasedForward(app, global_conf=global_conf,
                                                  mapper=mapper, **kw))


error_document_template = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
 <title>Server Error %(code)s</title>
 
<style type="text/css">
body {
  font-family: Helvetica, sans-serif;
}

table {
  width: 100%%;
}

tr.header {
  background-color: #006;
  color: #fff;
}

tr.even {
  background-color: #ddd;
}

table.variables td {
  verticle-align: top;
  overflow: auto;
}

a.button {
  background-color: #ccc;
  border: 2px outset #aaa;
  color: #000;
  text-decoration: none;
}

a.button:hover {
  background-color: #ddd;
}

code.source {
  color: #006;
}

a.switch_source {
  color: #0990;
  text-decoration: none;
}

a.switch_source:hover {
  background-color: #ddd;
}

.source-highlight {
  background-color: #ff9;
}

</style>

<!-- CSS Imports -->
<link rel="stylesheet" href="%(prefix)s/error/style/orange.css" type="text/css" media="screen" />

<!-- Favorite Icons -->
<link rel="icon" href="%(prefix)s/error/img/icon-16.png" type="image/png" />

<style type="text/css">
        .red {
            color:#FF0000;
        }
        .bold {
            font-weight: bold;
        }
</style>

</head>

<body id="documentation">
<!-- We are only using a table to ensure old browsers see the message correctly -->

<noscript>
<div style="border-bottom: 1px solid #808080">
<div style="border-bottom: 1px solid #404040">
<table width="100%%" border="0" cellpadding="0" bgcolor="#FFFFE1"><tr><td valign="middle"><img src="%(prefix)s/error/img/warning.gif" alt="Warning" /></td><td>&nbsp;</td><td><span style="padding: 0px; margin: 0px; font-family: Tahoma, sans-serif; font-size: 11px">Warning, your browser does not support JavaScript so you will not be able to use the interactive debugging on this page.</span></td></tr></table>
</div>
</div>
</noscript>
    
    <!-- Top anchor -->
    <a name="top"></a>
    
    <!-- Logo -->
    <h1 id="logo"><a class="no-underline" href="http://www.pylonshq.com"><img class="no-border" src="%(prefix)s/error/img/logo.gif" alt="Pylons" title="Pylons"/></a></h1>
    <p class="invisible"><a href="#content">Skip to content</a></p>

    <!-- Main Content -->

    <div id="nav-bar">

        <!-- Section Navigation -->
        <h4 class="invisible">Section Links</h4>

            <ul id="navlist">
                <li class="active"><a href="#" accesskey="1" class="active">Error %(code)s</a></li>
            </ul>
    </div>
    <div id="main-content">
    
        <div class="hr"><hr class="hr" /></div> 

        <div class="content-padding">
            
            <div id="main_data">
                <div style="float: left; width: 100%%; padding-bottom: 20px;">
                <h1 class="first"><a name="content"></a>Error %(code)s</h1>
                </div>
                
                %(message)s
                
            </div>

        </div>
        
        
            <!-- Footer -->

        <div class="hr"><hr class="clear" /></div>
    </div>
    
    <div style=" background: #FFFF99; padding: 10px 10px 10px 6%%; clear: both;">
        The Pylons Team | 
        <a href="#top" accesskey="9" title="Return to the top of the navigation links">Top</a>
    </div>
</body>
</html>
"""

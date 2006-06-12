"""Myghty compatibility object, ``etag_cache``, ``redirect_to`` and Myghty Module Components

Additional helper object available for use in Controllers is the etag_cache, along with
the Myghty compatibility objects for Pylons 0.8 projects and new Myghty Module Components
for use in Myghty templates.

"""
from paste.registry import StackedObjectProxy
import paste.httpexceptions as httpexceptions
from formencode import htmlfill

import pylons
import pylons.helpers
import pylons.templating as tmpl

response = StackedObjectProxy(name="response")

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to the response for use in future
    request cycles.
    
    Suggested use is within a Controller Action like so::
    
        import pylons
        
        class YourController(BaseController):
            def index(self):
                if pylons.etag_cache(key=1): return
                m.subexec('/splash.myt')
    
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    pylons.helpers.response.headers['ETag'] = key
    if str(key) == if_none_match:
        pylons.m.abort(304)
        return True
    else:
        return False

class Myghty_Compat(object):
    """Myghty Compatibility Object for Pylons 0.8 Projects"""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.headers_out = pylons.helpers.response.headers
        self.headers_in = pylons.request.headers
        self.request_args = pylons.request.params
    
    def write(self, content):
        pylons.helpers.response.write(content)
    
    def out(self, content):
        pylons.helpers.response.write(content)
    
    def cache_self(self, *args, **kargs):
        return False
    
    def subexec(self, *args, **kargs):
        pylons.helpers.response.write(tmpl.render(*args, **kargs))
    
    def comp(self, *args, **kargs):
        pylons.helpers.response.write(tmpl.render_fragment(*args, **kargs))
    
    def scomp(self, *args, **kargs):
        return tmpl.render_fragment(*args, **kargs)
    
    def fetch_component(self, name):
        return name
    
    def get_cache(self, component):
        return pylons.cache.get_cache(component)
    
    def send_redirect(self, path, hard=True):
        redirect_to(path)
    
    def abort(self, status_code=None, reason=""):
        if status_code == 404:
            raise httpexceptions.HTTPNotFound()
        else:
            return

def redirect_to(url):
    """Redirect function to raise an httpexception causing a 302 Redirect"""
    raise httpexceptions.HTTPFound(url)

def formfill(m, defaults=None, errors=None):
    """Formfill Myghty Module Component
    
    The Formfill module component is for use with Myghty as a wrapper
    around a ``<form>`` section. The formfill component will then parse
    the Myghty content block and fill in errors and defaults as needed.
    
    Formfill uses `FormEncode <http://formencode.org/>`_ to parse the
    form and put in errors and defaults.
    
    Example::
        
        <&| @pylons.helpers:formfill &>
        <form action="<% h.url_for() %>" method="post">
        Username: <input type="text" name="username" size="26" />
        <form:error name="username">
        Age: <input type="text" name="age" size="3" />
        <form:error name="age">
        <input type="submit" value="Send it" />
        </form>
        </&>
    
    """
    if not defaults:
        defaults = pylons.c.defaults
    if not errors:
        errors = pylons.c.errors
    form = m.content()
    m.write(htmlfill.render(form, defaults, errors))


__all__ = ['etag_cache', 'redirect_to', 'formfill']

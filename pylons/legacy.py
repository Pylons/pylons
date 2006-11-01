"""Legacy objects for Pylons 0.8 projects

Myghty compatibility object, old-style ``params`` and ``m`` globals. The
``response`` object is used to buffer the output.
"""
import types
import sys
import warnings

from paste.registry import StackedObjectProxy
import paste.httpexceptions as httpexceptions

import pylons
import pylons.templating as tmpl

# Legacy objects
m = StackedObjectProxy(name="m legacy object")
response = StackedObjectProxy(name="response")
params = StackedObjectProxy(name="params")

def load_h(package_name):
    """
    This is a legacy test for pre-0.9.3 projects to continue using the old
    style Helper imports. The proper style is to pass the helpers module ref
    to the PylonsApp during initialization.
    """
    warnings.warn(
        "Pylons 0.9.3 and above now passes the helpers module reference in "
        "directly. It's highly recommended that you update your middleware.py "
        "module so that the Pylons app load looks similar to:\n"
        "app = pylons.wsgiapp.PylonsApp(config, helpers=MYPROJ.lib.helpers, "
        "g=app_globals.Globals)\n"
        "Where MYPROJ is the name of your project. Also make sure to add an "
        "import line to the middleware.py to import the helpers modules:\n"
        "import MYPROJ.lib.helpers\n"
        "This will be required on all projects 1.0 and beyond.",
        DeprecationWarning, 2)
    __import__(package_name + '.lib.base')
    their_h = getattr(sys.modules[package_name + '.lib.base'], 'h', None)
    if isinstance(their_h, types.ModuleType):
        # lib.base.h is a module (and thus not pylons.h) -- assume lib.base uses
        # new style (self contained) helpers via:
        # import ${package}.lib.helpers as h
        return their_h

    # Assume lib.base.h is a StackedObjectProxy -- lib.base is using pre 0.9.2
    # style helpers via:
    # from pylons import h
    try:
        helpers_name = package_name + '.lib.helpers'
        __import__(helpers_name) 
    except ImportError:
        # pylons 0.8.x support
        helpers_name = package_name + '.config.helpers'
        __import__(helpers_name)
    helpers_module = sys.modules[helpers_name]

    # Pre 0.9.2 lib.helpers did not import the pylons helper functions, manually
    # add them. Don't overwrite user functions (allowing pylons helpers to be
    # overridden)
    for func_name in ('_', 'log', 'set_lang', 'get_lang'):
        if not hasattr(helpers_module, func_name):
            setattr(helpers_module, func_name, getattr(pylons.util, func_name))

    return sys.modules[helpers_name]
    
class MyghtyCompat(object):
    """Myghty Compatibility Object for Pylons 0.8 Projects"""
    def __init__(self, environ, start_response):
        """Create Myghty compatibility object given WSGI interface"""
        self.environ = environ
        self.start_response = start_response
        self.headers_out = response.headers
        self.headers_in = pylons.request.headers
        self.request_args = pylons.request._legacy_params
    
    def write(self, content):
        """Write content to the response buffer"""
        warnings.warn(
            "The m.write call has been deprecated. Replace with "
            "response.write() and instantiate a Response object.",
            DeprecationWarning, 2)
        response.write(content)
    out = write
    
    def cache_self(self, *args, **kargs):
        """Pretends to cache itself, actually disables caching"""
        warnings.warn(
            "The m.cache_self call has been deprecated. Replace usage of "
            "m.cache_self with return render_response() and add cache "
            "keywords.",
            DeprecationWarning, 2)
        return False
    
    def subexec(self, *args, **kargs):
        """Renders a template to the response buffer"""
        warnings.warn(
            "The m.subexec call has been deprecated. Replace with "
            "return render_response().",
            DeprecationWarning, 2)
        response.write(tmpl.render(*args, **kargs))
    
    def comp(self, *args, **kargs):
        """Renders a template fragment to the response buffer"""
        warnings.warn(
            "The m.comp call has been deprecated. Replace with return "
            "render_response('sometemplate.myt', fragment=True) or "
            "response.write(render('sometemplate.myt', fragment=True)) "
            "as necessary.",
            DeprecationWarning, 2)
        response.write(tmpl.render(fragment=True, *args, **kargs))
    
    def scomp(self, *args, **kargs):
        """Returns a rendered template fragment as a string"""
        warnings.warn(
            "The m.scomp call has been deprecated. Replace with result = "
            "render('sometemplate.myt', fragment=True).",
            DeprecationWarning, 2)
        return tmpl.render(fragment=True, *args, **kargs)
    
    def fetch_component(self, name):
        """Returns the name of the component"""
        warnings.warn(
            "The m.fetch_component call has been deprecated. See cache docs.",
            DeprecationWarning, 2)
        return name
    
    def get_cache(self, component):
        """Returns a cache namespace"""
        warnings.warn(
            "The m.get_cache call has been deprecated. See cache docs.",
            DeprecationWarning, 2)
        return pylons.cache.get_cache(component)
    
    def send_redirect(self, path, hard=True):
        """Raises a redirect exception for Paste HTTPExceptions"""
        warnings.warn(
            "The m.send_redirect call has been deprecated. Replace with "
            "redirect_to()",
            DeprecationWarning, 2)
        raise httpexceptions.HTTPFound(path)
    
    def abort(self, status_code=None, reason=""):
        """Raises a 404 or the given exception for Paste HTTPExceptions"""
        warnings.warn(
            "The m.abort call has been deprecated. Replace with "
            "abort(200, detail='some message').",
            DeprecationWarning, 2)
        if status_code == 404:
            raise httpexceptions.HTTPNotFound()
        else:
            exc = httpexceptions.get_exception(status_code)(detail=reason)
            raise exc

__all__ = ['m', 'params']

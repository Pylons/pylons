"""``etag_cache``, ``redirect_to``, and ``abort`` methods

Additional helper object available for use in Controllers is the etag_cache.
"""
import os.path
import paste.httpexceptions as httpexceptions
from paste.deploy.config import CONFIG
from routes import redirect_to

import pylons

def _(value):
    """Mark a string for translation
    
    Mark a string to be internationalized as follows:
    
    .. code-block:: Python
    
        h._('This should be in lots of languages')
    """
    return pylons.translator['translator'].gettext(value)

def log(msg):
    """Log a message to the output log."""
    pylons.request.environ['wsgi.errors'].write('=> %s\n'%str(msg))

def set_lang(lang):
    """Set the language used"""
    if lang is None:
        pylons.translator['translator'] = _Translator()
    else:
        from pkg_resources import resource_exists
        from pylons.i18n.translation import egg_translation
        project_name = CONFIG['app_conf']['package']
        catalog_path = os.path.join('i18n', lang, 'LC_MESSAGES')
        if not resource_exists(project_name, catalog_path):
            raise LanguageError('Language catalog %s not found' % \
                                os.path.join(project_name, catalog_path))
        pylons.translator['translator'] = \
            egg_translation(project_name, lang=catalog_path)

def get_lang():
    return pylons.translator.get('lang')

def etag_cache(key=None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``, then
    a ``304`` HTTP message will be returned with the ETag to tell the browser
    that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to a new response object and
    returned for use in your action.
    
    Suggested use is within a Controller Action like so:
    
    .. code-block:: Python
    
        import pylons
        
        class YourController(BaseController):
            def index(self):
                resp = etag_cache(key=1)
                resp.write(render('/splash.myt'))
                return resp
    
    .. Note:: 
        This works because etag_cache will raise an HTTPNotModified
        exception if the ETag recieved matches the key provided.
    """
    if_none_match = pylons.request.environ.get('HTTP_IF_NONE_MATCH', None)
    resp = pylons.Response()
    resp.headers['ETag'] = key
    if str(key) == if_none_match:
        raise httpexceptions.HTTPNotModified()
    else:
        return resp

def abort(status_code=None, detail="", headers=None, comment=None):
    """Aborts the request immediately by returning an HTTP exception
    
    In the event that the status_code is a 300 series error, the detail 
    attribute will be used as the Location header should one not be specified
    in the headers attribute.
    """
    exc = httpexceptions.get_exception(status_code)(detail, headers, comment)
    raise exc

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

class _Translator(object):
    """An empty gettext translator which just returns the original string"""
    def gettext(self, value):
        return value

__all__ = ['etag_cache', 'redirect_to', 'abort', '_', 'log', 'set_lang', 
           'get_lang']

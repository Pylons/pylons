"""Helpers object, Buffet template plug-in, RequestLocal object, and Paste Template config

The util module provides the main Helper object used by Pylons, in addition
to the Buffet object which enables usage of template engines supporting the
template plug-in scheme TurboGears utilizes.

The RequestLocal thread-local is utilized by Pylons as the ``c`` object that
is available via ``pylons.c`` and is cleared every request by Pylons.

PylonsTemplate is a Paste Template sub-class that configures the source directory and default
plug-ins for a new Pylons project.
"""
import sys
import os.path, gettext
import pkg_resources

from paste.script.templates import Template

import pylons

from routes import threadinglocal
from paste.deploy.config import CONFIG

available_engines = {}

for entry_point in pkg_resources.iter_entry_points('python.templating.engines'):
    Engine = entry_point.load()
    available_engines[entry_point.name] = Engine

def get_prefix(environ):
    prefix = environ['paste.config']['app'].get('prefix')
    if not prefix:
        if environ.get('SCRIPT_NAME', '') != '':
            prefix = environ['SCRIPT_NAME']
    if not prefix:
        prefix = ''
    return prefix

def run_wsgi(app, m, request, environ=None):
    if environ == None:
        environ = request.environ

    def pylons_response(status, headers, exc_info=None):
        request.status = status
        if exc_info != None:
            raise exc_info
        request.headers_out.clear()
        for h,v in headers:
            if h.lower() == 'content-type':
                request.content_type=v
            else:
                request.headers_out[h] = v

    for data in app(environ, pylons_response):
        m.write(data)

class RequestLocal(object):
    """This object emulates a dict and supports the full set of dict functions and operations.
    
    Internally, the dict is attached to a threading local object and
    all access is passed through to the thread-safe object.
    
    This difference means that the object must be initialized per-thread
    with a _clear() call before the object can be used, and it should be
    _clear()'ed every request call.
    
    The RequestLocal object also support attribute assignment, which is
    then internally stored as if they used item assignment. Attribute
    get is also supported, and is used to 'get' the name requested. Unlike
    normal attribute access, this will return an empty string if the
    attribute does not exist.
    """
    def __init__(self):
        self.__dict__['_local'] = threadinglocal.local()
        
    def __getattr__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            try:
                result = getattr(self._local.request, name)
            except AttributeError:
                result = self._local.request.get(name, '')
            return result
    
    def __setattr__(self, key, value):
        if key.startswith('_'):
            raise AttributeError("You cannot set attributes begining with '_' on the 'temp' object use temp['%s'] instead"%key)
            #object.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)
    
    def __len__(self):
        return self._local.request.__len__()
    
    def __getitem__(self, key):
        return self._local.request.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._local.request.__setitem__(key, value)
    
    def __delitem__(self, key):
        self._local.request.__delitem__(key)
    
    def __iter__(self):
        return self._local.request.__iter__()
    
    def __contains__(self, item):
        return self._local.request.__contains__(item)
    
    def _clear(self):
        self._local.request = {}
    
    def __repr__(self):
        return self._local.request.__repr__()

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

class _Translator(object):
    """An empty gettext translator which just returns the original string"""
    def gettext(self, value):
        return value

class Helpers(object):
    def __init__(self, **_pylons):
        self.__dict__['_local'] = RequestLocal()
        self.__dict__['_pylons'] = _pylons
    
    def __call__(self):
        """Initialize Helpers object for request with helpers module/object
        
        When called, the Helpers object will return itself, after initializing
        itself for the current thread/request. It is intended to be run at the
        begginning of every request to clear the thread local it uses and setup
        the helpers space that will be used for fetching helper names as well
        as translation.
        """
        self.__dict__['_local']._clear()
        project_name = CONFIG['app']['package']
        try:
            helpers_name = project_name + '.config.helpers'
            __import__(helpers_name)
        except:
            helpers_name = project_name + '.lib.helpers'
            __import__(helpers_name)
        helpers = sys.modules[helpers_name]
        self.__dict__['_local'].helpers = helpers
        self.__dict__['_local'].translator = _Translator()
        self.__dict__['_local'].config = CONFIG
        if CONFIG['app'].has_key('lang'):
            self.set_lang(CONFIG['app']['lang'])
        else:
            self.__dict__['_local'].lang = None
        return self
        
    def __getattr__(self, name):
        if hasattr(self.__dict__['_local'].helpers, name):
            return getattr(self.__dict__['_local'].helpers, name)
        elif name in self.__dict__['_local'].keys() and name != '_local' and len(str(name))>0 and str(name)[0] != '_':
            return getattr(self.__dict__['_local'],name)
        else:
            raise AttributeError('No such helper %s'%repr(name))
    
    def __setattr__(self, name, value):
        if name not in ['lang']:# or not self.__dict__['_local'].has_key(name):
            raise AttributeError("Helper attributes cannot be set. You should use the context object 'c' to store conext information.")
        else:
            self.set_lang(value)

    def log(self, msg):
        """Log a message to the output log."""
        self.__dict__['_pylons']['request'].environ['wsgi.errors'].write('=> %s\n'%str(msg))

    def translate(self, value):
        """Deprecated, use _()"""
        raise NotImplementedError('Use h._() instead')

    def _(self, value):
        """Mark a string for translation
        
        Mark a string to be internationalised as follows:
        
            h._('This should be in lots of langauges')
        """
        return self.__dict__['_local'].translator.gettext(value)
  
    def set_lang(self, lang):
        """Set the language used"""
        project_name = CONFIG['app']['package']
        self.__dict__['_local'].lang = lang
        if lang == None:
            self.__dict__['_local'].translator = _Translator()
        else:
            from pkg_resources import resource_string, resource_stream, resource_exists, resource_filename
            from pylons.i18n.translation import egg_translation
            if not resource_exists(project_name, 'i18n/%s/LC_MESSAGES'%(lang)):
                raise LanguageError(
                    'Langauge catalog %s not found'%repr(
                        '%s/i18n/%s/LC_MESSAGES'%(
                            project_name,
                            lang
                        )
                    )
                )
            self.__dict__['_local'].translator = egg_translation(
                project_name, 
                lang = 'i18n/%s/LC_MESSAGES'%(
                    lang
                )
            )

    def get_lang(self):
        return self.__dict__['_local'].lang

class BuffetError(Exception):
    pass

class Buffet(object):
    """Buffet style plug-in template rendering
    
    Buffet implements template language plug-in support modeled highly on the
    `Buffet Project <http://projects.dowski.com/projects/buffet>`_ from which
    this class inherits its name.
    """
    def __init__(self):
        self._local = RequestLocal()
    
    def _clear(self):
        self._local._clear()
    
    def prepare(self, engine_name, template_root=None):
        """Prepare a template engine for use
        
        This method must be run every request before the `render <#render>`_ method
        is called so that the ``template_root`` can be set.
        """
        Engine = available_engines.get(engine_name, None)
        if not Engine:
            raise TemplateEngineMissing('Please install a plugin for "%s" to use its functionality' % engine_name)
        setattr(self._local, engine_name, dict(engine=Engine(), root=template_root))
    
    def render(self, engine_name, template_name, as_string=False, include_pylons_variables=True, namespace=None, **options):
        """Render a template using a template engine plug-in
        
        To use templates it is expected that you will attach data to be used in
        the template to the ``c`` variable which is available in the controller
        and the template. 
        
        When porting code from other projects it is sometimes easier to use an
        exisitng dictionary which can be specified with ``namespace``.
        
        ``engine_name``
            The name of the template engine to use, which must be
            'prepared' first.
        ``template_name``
            Name of the template to render
        ``as_string``
            Whether or not to directly render the output to the browser, or
            return the rendered template as a string.
        ``include_pylons_variables``
            If a custom namespace is specified this determines whether Pylons 
            variables are included in the namespace or not. Defaults to ``True``.
        ``namespace``
            A custom dictionary of names and values to be substituted in the template.
            If ``include_pylons_variables`` is ``True`` and any keys in ``namespace`` 
            conflict with names of Pylons variables, an error is raised.
        
        All other keyword options are passed directly to the template engine
        used.
        """
        for char in ['/','\\']:
            if char in template_name:
                raise BuffetError('Templates should be specified as module paths relative to the '
                'template root and therefore cannot contain %s characters'%repr(char))

        def update_namespace(namespace):
            d = {}
            for k,v in namespace.items():
                d[k] = v
            d.update(
                dict(
                    c=pylons.c,
                    h=pylons.h,
                    m=pylons.m,
                    request=pylons.request,
                    g=pylons.request.environ['pylons.g'],
                    session=pylons.session,
                )
            )
            return d

        if namespace==None:
            if include_pylons_variables == False:
                raise BuffetError('You must specify ``namespace`` if ``include_pylons_variables`` is False')
            else:
                namespace = update_namespace({})
        elif isinstance(namespace, dict):
            if include_pylons_variables == True:
                keys = namespace.keys()
                for k in ['c','m','h','g','request','session']:
                    if k in keys:
                        raise Exception('The variable %s specified in namespace conflicts '
                            'with the Pylons variable of the same name. Set ``include_pylons_variables`` '
                            'to ``False`` if you do not want to use Pylons variables in your template'%k)
                namespace = update_namespace(namespace)
        else:
            namespace = update_namespace(namespace)
        engine_config = getattr(self._local, engine_name)
        base_path = engine_config['root'].split('/')
        tmpl_path = template_name.split('/')
        full_path = os.path.join(*(base_path + tmpl_path))
        dotted_path = full_path.replace(os.path.sep, '.').lstrip('.')
        page_data = engine_config['engine'].render(namespace, template=dotted_path, **options)
        if as_string:
            return page_data
        return pylons.m.write(page_data)
        
class TemplateEngineMissing(Exception):
    pass

class PylonsTemplate(Template):
    _template_dir = 'templates/paster_template'
    summary = 'Pylons application template'
    egg_plugins = ['Pylons', 'WebHelpers']

__all__ = ['RequestLocal', 'Helpers', 'Buffet']
__pudge_all__ = ['RequestLocal', 'Helpers', 'Buffet', 'PylonsTemplate']

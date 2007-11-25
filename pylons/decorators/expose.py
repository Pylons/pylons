import formencode
from paste.util.mimeparse import best_match
import pylons

def _schema(d=None, **kw):
    dd = {}
    if d:
        dd.update(d)
    dd.update(**kw)
    return formencode.Schema.__metaclass__('schema', (formencode.Schema,), dd)

class Decoration(object):

    def __init__(self):
        self.engines = {}
        self.validation = None
        self.error_handler = None
        self.hooks = dict(
            before_validate=[],
            before_call=[],
            before_render=[],
            after_render=[]
        )


    @classmethod
    def get_decoration(klass, func):
        if not hasattr(func, 'decoration'):
            func.decoration=klass()
        return func.decoration

    @property
    def exposed(self):
        if self.engines: return True
        else: return False

    def run_hooks(self, hook, *l, **kw):
        for func in self.hooks[hook]:
            func(*l, **kw)

    def register_template_engine(self, content_type, engine, template, exclude_names):
        '''Regesters an engine on the controller method.
        
        Multiple engines can be regestered for one controlelr method, but only one 
        engine per content_type.  If no content type is specified the engine is 
        regestered at */* which is the default, and will be used whenever 
        the controller does not regester a more specific response for the 
        content type specified in the accept header. 
        
        exclude_names keeps track of a list of keys which will be removed from the 
        controller's dictionary before it is loaded into the template.  This allows you to 
        exclude some information from JSONification, and other 'automatic' engines which 
        don't require a template.
        '''
        #TODO: Are there some other things like lookup paths which need to be setup here?
        if content_type is None:
            content_type = '*/*'
        self.engines[content_type] = engine, template, exclude_names

    def lookup_template_engine(self, request):
        '''Provides a convenience method to get the proper engine, content_type, template, 
        and exclude_names for a particular tg_format (which is pulled off of the request
        headers)."
        '''
        tg_format = request.headers.get('tg_format')
        if tg_format:
            assert '/' in tg_format, 'Invalid tg_format: must be a MIME type'
            accept_types = tg_format
        else: accept_types = request.headers.get('accept', '*/*')
        content_type = best_match(self.engines.keys(), accept_types)
        engine, template, exclude_names = self.engines[content_type]
        return content_type, engine, template, exclude_names

    def register_hook(self, hook_name, func):
        '''We now have four core hooks that can be applied by adding decorators: 
        before_validate, before_call, before_render, and after_render.   regester_hook attaches the
        function to the hook which get's called at the apropriate time in the request life cycle.)
        '''
        self.hooks[hook_name].append(func)

class _hook_decorator(object):
    hook_name=None # must be overridden

    def __init__(self, hook_func):
        self.hook_func = hook_func

    def __call__(self, func):
        deco = Decoration.get_decoration(func)
        deco.register_hook(self.hook_name, self.hook_func)
        return func

class before_validate(_hook_decorator):
    """"Provides a simple decorator based hook for actions which 
    should happen before validation."""
    hook_name = 'before_validate'
    
class before_call(_hook_decorator):
    """"Provides a simple decorator based hook for actions which 
    should happen the controller method is called."""
    hook_name = 'before_call'
    
class before_render(_hook_decorator):
    """"Provides a simple decorator based hook for actions which 
    should happen after the controller returns a dictionary, but before
    the template and engine are determined and the final output is rendered.
    """
    hook_name = 'before_render'
    
class after_render(_hook_decorator):
    """"Provides a simple decorator based hook for actions which 
    should happen at the end of the controller's call cycle, after
    the template has been rendered, imediately before controll is
    passed back up the WSGI call stack."""
    hook_name = 'after_render'

class expose(object):
    """
    regesters attributes on the decorated function
    
    :Parameters:

      template
        Assign an engine and a template file to use in rendering the response. 
        the syntax is "engine:template" but if engine is omitted, the template
        will be rendered using the default engine.
        
        The default template engine is genshi.

      content_type
        Assign the expected content type you are exposing with this template/engine.
        The default content type is 'text/html'.

      exclude_names
        exclude_names keeps track of a list of keys which will be removed from the 
        controller's dictionary before it is loaded into the template.  This allows you to 
        exclude some information from JSONification, and other 'automatic' engines which 
        don't require a template
        
    The expose decorator regesters a number of attributes on the decorated function, but 
    does not actually wrap the function the way TurboGears 1.0 style expose decorators did. 
    
    This means that we don't have to play any kind of special tricks to maintain the signature 
    of the exposed function.
    
    The exclude_names parameter is new, and it takes a list of keys that ought to be scrubbed
    from the dictinary before passing it on to the rendering engine.   This is particularly 
    usefull for JSON. 
    
    Expose decorator can be stacked like this::
    
        @expose('json', exclude_names='d')
        @expose('kid:blogtutorial.templates.test_form', content_type='text/html')
        def my_exposed_method(self):
            return dict(a=1, b=2, d="username")
    
    the expose('json') syntax is a special case.  json is a buffet rendering engine, but unlike others
    it does not require a template, and expose assumes that it matches content_type='application/json'
    
    Otherwise expose assumes that the template is for html.   All other content_types must 
    be explicitly matched to a template and engine.
    
    """
    def __init__(self, template='', content_type=None, exclude_names=None):
        if exclude_names is None:
            exclude_names = []    
        if template == 'json':
            engine, template = 'json', ''
        elif ':' in template:
            engine, template = template.split(':', 1)
        elif template:
            engine = 'genshi' 
            print "engine = %s" %engine
            
            template = template
        else:
            engine, template = None, None
            
        #If no content type is declared, assume that this exposes text/html
        if content_type is None:
            if engine == 'json': content_type = 'application/json'
            else: content_type = 'text/html'
        
        #Don't ever put the contents of the context object in the JSON output. 
        if engine == 'json' and 'context' not in exclude_names:
            exclude_names.append('context')
            
        #Assume UTF is charset if not explicitly declared    
        if 'charset' not in content_type: 
            content_type = '%s; charset=utf-8' % content_type        
        
        self.engine = engine
        self.template = template
        self.content_type = content_type
        self.exclude_names = exclude_names

    def __call__(self, func):
        deco = Decoration.get_decoration(func)
        deco.register_template_engine(
            self.content_type, self.engine, self.template, self.exclude_names)
        return func


class validate(object):
    """
    This validator can be used before or after an expose decorator, and 
    regesters information on the decoration object rather than wrapping 
    the functin itself.   We may not end up using this validator in the 
    final TG2 version."""
    
    def __init__(self, validators=None, error_handler=None):
        self.validators = validators
        self.error_handler = error_handler
        
    def __call__(self, func):
        deco = Decoration.get_decoration(func)
        deco.validation = self
        return func
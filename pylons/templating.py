"""Buffet templating plugin and render"""
import pkg_resources
import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from myghty.interp import Interpreter

import pylons

class BuffetError(Exception):
    pass

class Buffet(object):
    """Buffet style plug-in template rendering
    
    Buffet implements template language plug-in support modeled highly on the
    `Buffet Project <http://projects.dowski.com/projects/buffet>`_ from which
    this class inherits its name.
    
    """
    def __init__(self, default_engine=None, template_root=None, 
        default_options={}, **config):
        """Initialize the Buffet renderer, and optionally set a default
        engine/options"""
        self.default_engine = default_engine
        self.template_root = template_root
        self.default_options = default_options
        self.engines = {}
        if self.default_engine:
            self.prepare(default_engine, template_root, **config)
        
    def prepare(self, engine_name, template_root=None, **config):
        """Prepare a template engine for use
        
        This method must be run every request before the `render <#render>`_
        method is called so that the ``template_root`` can be set.
        
        """
        Engine = available_engines.get(engine_name, None)
        if not Engine:
            raise TemplateEngineMissing('Please install a plugin for '
                '"%s" to use its functionality' % engine_name)
        defaults = config.pop('default_options', None)
        self.engines[engine_name] = \
            dict(engine=Engine(options=config), root=template_root)
    
    def _update_names(self, ns):
        d = {}
        d.update(ns)
        d.update(dict(
            c=pylons.c,
            h=pylons.h,
            m=pylons.m,
            request=pylons.request,
            g=pylons.g,
            session=pylons.session,
        ))
        return d
    
    def render(self, engine_name=None, template_name=None, 
        include_pylons_variables=True, namespace=None, **options):
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
        ``include_pylons_variables``
            If a custom namespace is specified this determines whether Pylons 
            variables are included in the namespace or not. Defaults to 
            ``True``.
        ``namespace``
            A custom dictionary of names and values to be substituted in the
            template. If ``include_pylons_variables`` is ``True`` and any
            keys in ``namespace`` conflict with names of Pylons variables, 
            an error is raised.
        
        All other keyword options are passed directly to the template engine
        used.
        
        """
        if not engine_name and self.default_engine:
            engine_name = self.default_engine
        engine_config = self.engines.get(engine_name)
        full_path = template_name
        
        if engine_name != 'pylonsmyghty':
            if namespace==None:
                if include_pylons_variables is False:
                    raise BuffetError('You must specify ``namespace`` if ``include_pylons_variables`` is '
                                      'False')
                else:
                    namespace = self._update_names({})
            elif isinstance(namespace, dict):
                if include_pylons_variables is True:
                    for k in ['c','h','g','request','session', 'params']:
                        if k in namespace:
                            raise Exception('The variable %s specified in namespace conflicts '
                                'with the Pylons variable of the same name. Set ``include_pylons_variables`` '
                                'to ``False`` if you do not want to use Pylons variables in your template'%k)
                    namespace = self._update_names(namespace)
            else:
                namespace = self._update_names(namespace)
            full_path = os.path.join(engine_config['root'], template_name)
            full_path = full_path.replace(os.path.sep, '.').lstrip('.')
        return engine_config['engine'].render(namespace, template=full_path, **options)
        
class TemplateEngineMissing(Exception):
    pass

class MyghtyTemplatePlugin(object):
    extension = "myt"

    def __init__(self, extra_vars_func=None, options={}):
        myt_opts = {}
        for k, v in options.iteritems():
            myt_opts[k[7:]] = v
        myt_opts['global_args'] = dict(
            c=pylons.c,
            h=pylons.h,
            request=pylons.request,
            g=pylons.g,
            session=pylons.session,
        )
        self.interpreter = Interpreter(**myt_opts)
    
    def load_template(self, template_path):
        pass

    def render(self, info, format="html", fragment=False, template=None):
        vars = info
        buf = StringIO()
        if fragment:
            self.interpreter.execute(template, request_args=vars, out_buffer=buf, disable_wrapping=True)
        else:
            self.interpreter.execute(template, request_args=vars, out_buffer=buf)
        return buf.getvalue()

available_engines = {}

for entry_point in pkg_resources.iter_entry_points('python.templating.engines'):
    Engine = entry_point.load()
    available_engines[entry_point.name] = Engine

def render(*args, **kargs):
    args = list(args)
    template = args.pop()
    if args: 
        engine = args.pop()
        return pylons.buffet.render(engine, template, namespace=kargs)
    return pylons.buffet.render(template_name=template, namespace=kargs)

def render_fragment(*args, **kargs):
    args = list(args)
    template = args.pop()
    if args: 
        engine = args.pop()
        return pylons.buffet.render(engine, template, fragment=True, namespace=kargs)
    return pylons.buffet.render(template_name=template, fragment=True, namespace=kargs)

def render_response(*args, **kargs):
    return pylons.Response(render(*args, **kargs))

def render_response_fragment(*args, **kargs):
    return pylons.Response(render_fragment(*args, **kargs))    

"""Myghty Routes Resolver and ComponentSource classes for controllers

MyghtyRoutes implements Routes-based dispatching and controller setup
using subclasses of Myghty ModuleComponentSource with a custom resolver
called RoutesResolver.

The custom Myghty Routes Resolver is used with Myghty's `Advanced Resolver
Configuration <http://www.myghty.org/docs/resolver.myt>`_ and is setup in
`pylons.config <module-pylons.config.html#pylons_config>`_.

The ComponentSource and RoutesComponentSource classes are used to setup the
controller and environment thread-locals for every request. They also ensure
that the controller is reloaded if the file has been updated.
"""

import os
import string
import re, inspect

from myghty.resolver import ResolverRule
import myghty.csource as csource
import myghty.component as comp
from myghty.resolver import Resolution
import myghty.importer as importer
import myghty.escapes as escapes
from myghty import request

from routes import request_config

from pylons.util import *
import pylons.controllers as controllers
import pylons

class RoutesComponentSource(csource.ModuleComponentSource):
    """Holds a reference to the controller source file
    
    If the source file is updated, the module will be reloaded
    """
    def __init__(self, objpath, module):
        arg = module
        for t in objpath:
            arg = getattr(arg, t)
        
        name = "class:" + objpath[0]
        
        self.has_method = False
        last_modified = importer.mod_time(module)
        
        csource.ComponentSource.__init__(self, "module|%s:%s" % (module.__name__, name), last_modified = last_modified)
        
        self.module = module
        self.objpath = objpath
        self.name = name
        self.class_ = RoutesComponent
        self.callable_ = arg
    
    def reload(self, module):
        self.module = module        

        arg = module
        for t in self.objpath:
            arg = getattr(arg, t)
        self.callable_ = arg
    
    def can_compile(self):
        return False

class RoutesComponent(comp.ModuleComponent):
    """Makes the Controller act like a ModuleComponent
    
    The RoutesComponent holds a reference to the Controller object,
    and instantiates/calls it during the request cycle. The environ
    dict is also setup here.
    """
    def component_init(self):
        self.callable_ = self.component_source.callable_
    
    def do_run_component(self, m, r, **params):
        # Clear thread-locals
        pylons.c._clear()
        pylons.buffet._clear()
        
        # Setup matchargs
        matchargs = m.resolution.override_args.copy()
        matchargs['ARGS'] = params['ARGS']
        
        # Setup Myghty globals
        m.global_args.update(dict(session=pylons.session,
                                  request=pylons.request,
                                  c=pylons.c,
                                  h=pylons.h(),
                                  s=pylons.session,
                                  g=pylons.request.environ.get('pylons.g'))
                            )
        # Setup testing info if using paste fixture testing
        if r.environ.get('paste.testing'):
            self._load_test_env(r, m, params)
                
        if inspect.isclass(self.callable_) and issubclass(self.callable_, controllers.Controller):
            controller = self.callable_() # Instantiate the controller
            controller.c = pylons.c
            return controller(**matchargs)
        else:
            self.run_wsgi_app(self.callable_, **matchargs)
    
    def run_wsgi_app(self, controller, **params):
        # pylons.g key already there
        env = pylons.request.environ
        env['myghty.r'] = pylons.request
        env['myghty.m'] = pylons.m
        env['myghty.s'] = pylons.session
        env['pylons.h'] = pylons.h
        env['pylons.m'] = env['myghty.m']
        env['pylons.request'] = env['myghty.r']
        env['pylons.session'] = env['myghty.s']
        
        # Fixup the PATH_INFO and SCRIPT_NAME if we have a url parameter
        config = request_config()
        oldpath = env['PATH_INFO']
        newpath = params.get('path_info') or params.get('url') or ''
        env['PATH_INFO'] = newpath
        if not env['PATH_INFO'].startswith('/'):
            env['PATH_INFO'] = '/' + env['PATH_INFO']
        env['SCRIPT_NAME'] += re.sub(r'^(.*?)/' + newpath + '$', r'\1', oldpath)
        if env['SCRIPT_NAME'].endswith('/'):
            env['SCRIPT_NAME'] = env['SCRIPT_NAME'][:-1]
        
        from pylons.util import run_wsgi
        run_wsgi(controller, pylons.m._get_object(), pylons.request._get_object(), env)
    
    def _load_test_env(self, r, m, params):
        """Sets up our Paste testing environment and Myghty mock objects"""
        testenv = r.environ['paste.testing_variables']
        testenv['session'] = m.get_session()
        testenv['request'] = r
        testenv['m'] = m
        comprecord = testenv['comp_calls'] = []
        def test_comp(func, call_name, comprecord):
            def record_call(*args, **kw):
                comprecord.append(dict(comptype=call_name, template=args[0], params=kw))
                return func(*args, **kw)
            return record_call
        m.comp = test_comp(m.comp, 'comp', comprecord)
        m.scomp = test_comp(m.scomp, 'scomp', comprecord)
        def test_subrequest(func, comprecord):
            def record_subreq(*args, **kw):
                comprecord.append(dict(comptype='subrequest', template=args[0], params=kw))
                return func(*args, **kw)
            return record_subreq
        m.make_subrequest = test_subrequest(m.make_subrequest, comprecord)
        testenv['params'] = params
  

class RoutesResolver(ResolverRule):
    """A Myghty ResolverRule Subclass that implements Routes-base dispatching
    
    RoutesResolver subclasses ResolverRule and is used to implement Routes-based
    dispatching. The RoutesResolver currently is heavily bound to the Pylons
    run-time environment and is not usable outside of Pylons.
    """
    name = 'routeresolver'
    
    def __init__(self, mapper=None, controller_root=None, scan_controllers=False, **params):
        """Initialize the RoutesResolver
        
        ``mapper``
            Store a reference to the mapper used for this application
        ``controller_root``
            Used to locate the controller module to load
        ``scan_controllers``
            Indicates whether the controllers dir should be scanned every reuqest
        """
        self.mapper = mapper
        self.controller_root = controller_root
        self.scan_controllers = scan_controllers
    
    def do_init_resolver(self, resolver, remaining_rules, **params):
        """Myghty Routes Resolver init
        
        Called by Myghty to initialize the RoutesResolver. Also initializes the
        Pylons module globals.
        """
        self.mapper.always_scan = self.scan_controllers
    
    def do(self, uri, remaining, resolution_detail, **params):
        """Called per-Request by Myghty to Resolve the uri"""
        
        if resolution_detail is not None: resolution_detail.append("resolverouteresolver:" + uri)
        
        config = request_config()
        config.mapper = self.mapper
        m = request.instance()
        env = m.request_impl.httpreq.environ
        env['PATH_INFO'] = uri
        config.environ = env
        match = config.mapper_dict
        if match:
            config.redirect = m.send_redirect
            
            controller = match['controller']
            action = match['action']
            if action.startswith('_'):
                return remaining.next().do(uri, remaining, resolution_detail, **params)
            
            # Sanitaze keys
            for k,v in match.iteritems():
                if v:
                    match[k] = escapes.url_unescape(v)
            
            match = match.copy()
            # Remove the action/controller, rest of the args pass to the function
            del match['controller']
            
            filename = self.controller_root + '/' + controller + '.py'
            controller_name = controller.split('/')[-1].title().replace('-', '_') 
            classname = controller_name + 'Controller' 
            
            module = importer.filemodule(filename)
            resolution_detail.append("\nController:%s, Action:%s" % (controller, action))
            cs = RoutesComponentSource(
                module=module,
                objpath=[classname],
                )
            #raise repr(cs.__dict__)
            return Resolution(cs, resolution_detail, override_args = match)
        else:
            return remaining.next().do(uri, remaining, resolution_detail, **params)

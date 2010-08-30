"""Configuration object and defaults setup

The PylonsConfig object is initialized in pylons projects inside the
:file:`config/environment.py` module. Importing the :data:`config`
object from module causes the PylonsConfig object to be created, and
setup in  app-safe manner so that multiple apps being setup avoid
conflicts.

After importing :data:`config`, the project should then call
:meth:`~PylonsConfig.init_app` with the appropriate options to setup
the configuration. In the config data passed with
:meth:`~PylonsConfig.init_app`, various defaults are set use with Paste
and Routes.

"""
import copy
import functools
import inspect
import logging
import os
import re

from paste.config import DispatchingConfig
from paste.deploy.converters import asbool
from webhelpers.mimehelper import MIMETypes

from repoze.bfg.configuration import Configurator as BFGConfigurator
from repoze.bfg.exceptions import ConfigurationError
from repoze.bfg.threadlocal import get_current_registry
from repoze.bfg.threadlocal import get_current_request

from repoze.bfg.mako import renderer_factory as mako_renderer_factory

from pylons.controllers.util import Request
from pylons.events import TemplateGlobals
from pylons.util import resolve_dotted
from pylons.url import route_url



request_defaults = dict(charset='utf-8', errors='replace',
                        decode_param_names=False, language='en-us')
response_defaults = dict(content_type='text/html',
                         charset='utf-8', errors='strict', 
                         headers={'Cache-Control': 'no-cache', 
                                  'Pragma': 'no-cache'})

log = logging.getLogger(__name__)


config = DispatchingConfig()

class PylonsConfig(dict):
    """Pylons configuration object

    The Pylons configuration object is a per-application instance
    object that retains the information regarding the global and app
    conf's as well as per-application instance specific data such as
    the mapper, and the paths for this instance.

    The config object is available in your application as the Pylons
    global :data:`pylons.config`. For example::

        from pylons import config

        template_paths = config['pylons.paths']['templates']

    There's several useful keys of the config object most people will
    be interested in:

    ``pylons.paths``
        A dict of absolute paths that were defined in the applications
        ``config/environment.py`` module.
    ``pylons.environ_config``
        Dict of environ keys for where in the environ to pickup various
        objects for registering with Pylons. If these are present then
        PylonsApp will use them from environ rather than using default
        middleware from Beaker. Valid keys are: ``session, cache``
    ``pylons.strict_tmpl_context``
        Whether or not the ``tmpl_context`` object should throw an
        attribute error when access is attempted to an attribute that
        doesn't exist. Defaults to True.
    ``pylons.tmpl_context_attach_args``
        Whethor or not Routes variables should automatically be
        attached to the tmpl_context object when specified in a
        controllers method.
    ``pylons.request_options``
        A dict of Content-Type related default settings for new
        instances of :class:`~pylons.controllers.util.Request`. May
        contain the values ``charset`` and ``errors`` and 
        ``decode_param_names``. Overrides the Pylons default values
        specified by the ``request_defaults`` dict.
    ``pylons.response_options``
        A dict of Content-Type related default settings for new 
        instances of :class:`~pylons.controllers.util.Response`. May
        contain the values ``content_type``, ``charset`` and
        ``errors``. Overrides the Pylons default values specified by
        the ``response_defaults`` dict.
    ``routes.map``
        Mapper object used for Routing. Yes, it is possible to add
        routes after your application has started running.
    
    """
    defaults = {
        'debug': False,
        'pylons.package': None,
        'pylons.paths': {'root': None,
                         'controllers': None,
                         'templates': [],
                         'static_files': None},
        'pylons.environ_config': dict(session='beaker.session', 
                                      cache='beaker.cache'),
        'pylons.app_globals': None,
        'pylons.h': None,
        'pylons.request_options': request_defaults.copy(),
        'pylons.response_options': response_defaults.copy(),
        'pylons.strict_tmpl_context': True,
        'pylons.tmpl_context_attach_args': False,
    }
    
    def init_app(self, global_conf, app_conf, package=None, paths=None):
        """Initialize configuration for the application
        
        .. note
            This *must* be called at least once, as soon as possible 
            to setup all the configuration options.
        
        ``global_conf``
            Several options are expected to be set for a Pylons web
            application. They will be loaded from the global_config 
            which has the main Paste options. If ``debug`` is not 
            enabled as a global config option, the following option
            *must* be set:

            * error_to - The email address to send the debug error to

            The optional config options in this case are:

            * smtp_server - The SMTP server to use, defaults to 
              'localhost'
            * error_log - A logfile to write the error to
            * error_subject_prefix - The prefix of the error email
              subject
            * from_address - Whom the error email should be from
        ``app_conf``
            Defaults supplied via the [app:main] section from the Paste
            config file. ``load_config`` only cares about whether a 
            'prefix' option is set, if so it will update Routes to
            ensure URL's take that into account.
        ``package``
            The name of the application package, to be stored in the 
            app_conf.
        
        .. versionchanged:: 1.0
            ``template_engine`` option is no longer supported.
                
        """
        log.debug("Initializing configuration, package: '%s'", package)
        
        conf = global_conf.copy()
        conf.update(app_conf)
        conf.update(dict(app_conf=app_conf, global_conf=global_conf))
        conf.update(self.pop('environment_load', {}))

        if paths:
            conf['pylons.paths'] = paths
        
        conf['pylons.package'] = package
        
        conf['debug'] = asbool(conf.get('debug'))
                
        # Load the MIMETypes with its default types
        MIMETypes.init()
        
        # Ensure all the keys from defaults are present, load them if not
        for key, val in copy.deepcopy(PylonsConfig.defaults).iteritems():
            conf.setdefault(key, val)

        # Load the errorware configuration from the Paste configuration file
        # These all have defaults, and emails are only sent if configured and
        # if this application is running in production mode
        errorware = {}
        errorware['debug'] = conf['debug']
        if not errorware['debug']:
            errorware['debug'] = False
            errorware['error_email'] = conf.get('email_to')
            errorware['error_log'] = conf.get('error_log', None)
            errorware['smtp_server'] = conf.get('smtp_server',
                'localhost')
            errorware['error_subject_prefix'] = conf.get(
                'error_subject_prefix', 'WebApp Error: ')
            errorware['from_address'] = conf.get(
                'from_address', conf.get('error_email_from',
                                         'pylons@yourapp.com'))
            errorware['error_message'] = conf.get('error_message',
                'An internal server error occurred')

        # Copy in some defaults
        if 'cache_dir' in conf:
            conf.setdefault('beaker.session.data_dir',
                            os.path.join(conf['cache_dir'], 'sessions'))
            conf.setdefault('beaker.cache.data_dir',
                            os.path.join(conf['cache_dir'], 'cache'))

        conf['pylons.cache_dir'] = conf.pop('cache_dir', 
                                            conf['app_conf'].get('cache_dir'))
        # Save our errorware values
        conf['pylons.errorware'] = errorware
        
        # Load conf dict into self
        self.update(conf)


pylons_config = PylonsConfig()


# Push an empty config so all accesses to config at import time have something
# to look at and modify. This config will be merged with the app's when it's
# built in the paste.app_factory entry point.
pylons_config.update(copy.deepcopy(PylonsConfig.defaults))
config.push_process_config(pylons_config)

def globals_factory(system):
    req = system['request']
    if req is None:
        registry = get_current_registry()
        req = get_current_request()
        system['request'] = req
    else:
        registry = req.registry
    d = {
        'url': route_url,
        'h': registry.helpers,
    }
    if req:
        d['c'] = req.tmpl_context
        d['tmpl_context'] = req.tmpl_context
        if 'session' in req.__dict__:
            d['session'] = req.session
    
    has_listeners = registry.has_listeners
    has_listeners and registry.notify(TemplateGlobals(d))
    return d


class Configurator(BFGConfigurator):

    pylons_route_re = re.compile(r'(/{[a-zA-Z]\w*})')

    def __init__(self, *arg, **kw):
        result = BFGConfigurator.__init__(self, *arg, **kw)
        for extension in ('.mak', '.mako'):
            self.add_renderer(extension, mako_renderer_factory)
        self.set_renderer_globals_factory(globals_factory)
        self.registry.helpers = None
        self.set_request_factory(Request)
        return result
    
    def add_helpers(self, module_ref):
        """ Add a reference to the helpers module, or load the module
        ref if its a dotted notation string."""
        if isinstance(module_ref, basestring):
            module_ref = resolve_dotted(module_ref)
        self.registry.helpers = module_ref

    def add_route(self, name, pattern, **kw):
        """ Support the syntax supported by
        :meth:`repoze.bfg.configuration.Configurator.add_route` but
        also support the ``/{squiggly}`` segment syntax by
        transforming it into ``/:colon``-style syntax. """
        parts = self.pylons_route_re.split(pattern)
        npattern = []

        for part in parts:
            match = self.pylons_route_re.match(part)
            if match:
                npattern.append('/:%s' % match.group()[2:-1])
            else:
                npattern.append(part)

        npattern = ''.join(npattern)

        return BFGConfigurator.add_route(self, name, npattern, **kw)

    def add_handler(self, route_name, pattern, handler, action=None, **kw):
        """ Add a Pylons handler.  This function adds a route and some
        number of views based on a handler object (usually a class).
        
        ``route_name`` is the name of the route (to be used later in
        URL generation).

        ``pattern`` is the matching pattern, e.g. ``'/blog/{action}'``
        
        ``handler`` is a dotted name of (or direct reference to) a
        Python handler class,
        e.g. ``'my.package.handlers.MyHandler'``.

        If ``{action}`` or ``:action`` is in
        the pattern, the exposed methods of the handler will be used
        as views.

        If ``action`` is passed, it will be considered the method name
        of the handler to use as a view.

        Passing both ``action`` and having an ``{action}`` in the
        route pattern is disallowed.

        Any extra keyword arguments are passed along to ``add_route``.

        This method returns the result of add_route."""
        if isinstance(handler, basestring):
            handler = resolve_dotted(handler)

        route = self.add_route(route_name, pattern, **kw)

        path_has_action = ':action' in pattern or '{action}' in pattern

        if action and path_has_action:
            raise ConfigurationError(
                'action= (%r) disallowed when an action is in the route '
                'path %r' % (action, pattern))

        if path_has_action:
            autoexpose = getattr(handler, '__autoexpose__', r'[A-Za-z]+')
            if autoexpose:
                try:
                    autoexpose = re.compile(autoexpose).match
                except (re.error, TypeError), why:
                    raise ConfigurationError(why[0])
            for method_name, method in inspect.getmembers(
                handler, inspect.ismethod):
                configs = getattr(method, '__exposed__', [])
                if autoexpose and not configs:
                    if autoexpose(method_name):
                        configs = [{}]
                for expose_config in configs:
                    # we don't want to mutate any dict in __exposed__,
                    # so we copy each
                    view_args = expose_config.copy()
                    action = view_args.pop('name', method_name)
                    preds = list(view_args.pop('custom_predicates',[]))
                    preds.append(ActionPredicate(action))
                    view_args['custom_predicates'] = preds
                    self.add_view(view=handler, attr=method_name,
                                  route_name=route_name, **view_args)
        else:
            method_name = action
            if method_name is None:
                method_name = '__call__'
            
            # Scan the controller for any other methods with this action name
            for meth_name, method in inspect.getmembers(
                handler, inspect.ismethod):
                configs = getattr(method, '__exposed__', [{}])
                for expose_config in configs:
                    # Don't re-register the same view if this method name is
                    # the action name
                    if meth_name == action:
                        continue
                    # We only reg a view if the name matches the action
                    if expose_config.get('name') != method_name:
                        continue
                    # we don't want to mutate any dict in __exposed__,
                    # so we copy each
                    view_args = expose_config.copy()
                    del view_args['name']
                    self.add_view(view=handler, attr=method_name,
                                  route_name=route_name, **view_args)
            
            # Now register the method itself
            method = getattr(handler, method_name, None)
            configs = getattr(method, '__exposed__', [{}])
            for expose_config in configs:
                self.add_view(view=handler, attr=action, route_name=route_name,
                              **expose_config)

        return route

    def add_rest_handler(self, collection_name, member_name, handler):
        """ Add a special kind of handler, a 'REST handler`.

        A 'REST handler' is a class that has a particular interface.
        This is the interface::

          class MyRestHandler(object):
              def __init__(self, request):
                  self.request = request
                  
              def index(self):
                  ''' Return an index of links to members '''

              def create(self):
                  ''' Create a new member '''

              def new(self):
                  ''' Returns a new member prototoype '''

              def update(self, id):
                  ''' Update a member '''

              def delete(self, id):
                  ''' Delete a member '''

              def show(self, id):
                  ''' Show a member '''

              def edit(self, id):
                  ''' Edit a member '''

        All methods should return a Python object, which will be
        serialized to JSON (or a webob.Response, which will not be).

        The configuration call for
        ``config.add_rest_handler('message', 'messages', Messages)``
        is shortcut for a set of ``add_route`` calls which makes the
        following result table true where ``messages`` below is an
        instance of the ``Messages`` class::

          GET    /messages        => messages.index()    => url("messages")
          POST   /messages        => messages.create()   => url("messages")
          GET    /messages/new    => messages.new()      => url("new_message")
          PUT    /messages/1      => messages.update(id) => url("message", id=1)
          DELETE /messages/1      => messages.delete(id) => url("message", id=1)
          GET    /messages/1      => messages.show(id)   => url("message", id=1)
          GET    /messages/1/edit => messages.edit(id)   => url("edit_message", id=1)

        XXX need a lot more docs

        """
        if isinstance(handler, basestring):
            handler = resolve_dotted(handler)

        handler = self._make_rest_handler(handler)
        add = functools.partial(self.add_route, view_renderer='json',
                                view=handler)
        add(collection_name, collection_name,
            request_method='GET', view_attr='index')
        add(collection_name + '_create', collection_name,
            request_method='POST', view_attr='create')
        add('new_%s' % member_name, '%s/new' % collection_name,
            request_method='GET', view_attr='new')
        add(member_name, '%s/:id' % collection_name,
            request_method='GET', view_attr='show')
        add(member_name + '_update', '%s/:id' % collection_name,
            request_method='PUT', view_attr='update')
        add(member_name + '_delete', '%s/:id' % collection_name,
            request_method='DELETE', view_attr='delete')
        add('edit_%s' % member_name, '%s/:id/edit' % collection_name,
            request_method='GET', view_attr='edit')
        return handler

    def _make_rest_handler(self, handler_factory):
        class RestHandlerWrapper(object):
            factory = handler_factory
            def __init__(self, request):
                self.request = request
                
            def _get_handler(self):
                handler =  handler_factory(self.request)
                return handler

            def index(self):
                handler = self._get_handler()
                return handler.index()

            def create(self):
                handler = self._get_handler()
                return handler.create()

            def new(self):
                handler = self._get_handler()
                return handler.new()

            def update(self):
                handler = self._get_handler()
                id = self.request.matchdict['id']
                return handler.update(id)

            def delete(self):
                handler = self._get_handler()
                id = self.request.matchdict['id']
                return handler.delete(id)

            def show(self):
                handler = self._get_handler()
                id = self.request.matchdict['id']
                return handler.show(id)

            def edit(self):
                handler = self._get_handler()
                id = self.request.matchdict['id']
                return handler.edit(id)

        return RestHandlerWrapper

class ActionPredicate(object):
    action_name = 'action'
    def __init__(self, action):
        try:
            self.action_re = re.compile(action + '$')
        except (re.error, TypeError), why:
            raise ConfigurationError(why[0])

    def __call__(self, context, request):
        matchdict = getattr(request, 'matchdict', None)
        if matchdict is None:
            return False
        action = matchdict.get(self.action_name)
        if action is None:
            return False
        return bool(self.action_re.match(action))
        

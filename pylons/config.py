"""Configuration setup for templating systems and Paste error
middleware

This module supplies pylons_config which handles setting up defaults
for templating systems, Paste errorware, and prefixing Routes if
necessary.
"""
import os
import re
import warnings

from paste.deploy.converters import asbool

import pylons.legacy
import pylons.templating

request_defaults = dict(charset=None, errors='strict',
                        decode_param_names=False,
                        language='en-us')
response_defaults = dict(content_type='text/html',
                         charset='utf-8', errors='strict')

class Config(object):
    """Pylons configuration object
    
    The Pylons configuration object is a per-application instance object
    that retains the information regarding the global and app conf's as
    well as per-application instance specific data such as the mapper, the
    paths for this instance, and the myghty configuration.
    
    The Config object is available in your application as a Pylons global
    ``pylons_config`` under the ``g`` object. There's several useful
    attributes of the config object most people will be interested in:
    
    ``tmpl_options``
        Full dict of template options that any TG compatible plugin should
        be able to parse. Comes with basic config needed for Myghty, Kid,
        and Mako.
    ``map``
        Mapper object used for Routing. Yes, it is possible to add routes
        after your application has started running.
    ``paths``
        A dict of absolute paths that were defined in the applications
        ``config/environment.py`` module.
    ``environ_config``
        Dict of environ keys for where in the environ to pickup various
        objects for registering with Pylons. If these are present then
        PylonsApp will use them from environ rather than using default
        middleware from Beaker. Valid keys are: ``session, cache``
    ``template_engines``
        List of template engines to configure. The first one in the list will
        be configured as the default template engine. Each item in the list is
        a dict indicating how to configure the template engine with keys:
        ``engine``, ``template_root``, ``template_options``, and ``alias``
    ``default_charset``
        Deprecated: Use the response_settings dict instead.
        Default character encoding specified to the browser via the
        'charset' parameter of the HTTP response's Content-Type header.
    ``strict_c``
        Whether or not the ``c`` object should throw an attribute error when
        access is attempted to an attribute that doesn't exist.
    ``request_settings``
        A dict of Content-Type related default settings for new instances of
        ``paste.wsgiwrappers.WSGIRequest``. May contain the values ``charset``
        and ``errors`` and ``decode_param_names``. Overrides the Pylons default
        values specified by the ``request_defaults`` dict.
    ``response_settings``
        A dict of Content-Type related default settings for new instances of
        ``pylons.Response``. May contain the values ``content_type``,
        ``charset`` and ``errors``. Overrides the Pylons default values
        specified by the ``response_defaults`` dict.
    ``global_conf``
        Global configuration passed in from Paste, this corresponds to the
        DEFAULTS section in the config file.
    ``app_conf``
        Application specific configuration directives, passed in via Paste
        from the app section of the config file.
    """
    def __init__(self, tmpl_options=None, map=None, paths=None, 
                 environ_config=None, default_charset=None, strict_c=False,
                 request_settings=None, response_settings=None):
        if paths is None:
            paths = {}
        if tmpl_options is None:
            tmpl_options = {}
        if environ_config is None:
            environ_config = {}
        self.myghty = tmpl_options
        self.template_options = tmpl_options
        self.map = map
        self.paths = paths
        self.environ_config = environ_config
        self.strict_c = strict_c
        self.helpers = None

        self.request_settings = request_defaults.copy()
        if request_settings:
            self.request_settings.update(request_settings)
        self.response_settings = response_defaults.copy()
        if response_settings:
            self.response_settings.update(response_settings)

        self.global_conf = {}
        self.app_conf = {}
        self.template_engines = []
        self._clean_tmpl_options()

        if default_charset is not None:
            warnings.warn(pylons.legacy.default_charset_warning % \
                              dict(klass='Config', charset=default_charset),
                          DeprecationWarning, 2)
            self.response_settings['charset'] = default_charset
    
    def _clean_tmpl_options(self):
        """Prase the template options, set self.myghty to have myghty options
        with no prefix and template_options to be a proper set of options for 
        any template engine"""
        oldopts = self.myghty
        self.template_options = {}
        self.myghty = {}
        for k, v in oldopts.iteritems():
            if not re.match(r'\w+\.\w*', k):
                self.myghty[k] = v
            elif k.startswith('myghty.'):
                self.myghty[k[7:]] = v
            else:
                self.template_options[k] = v
    
    def add_template_engine(self, engine, root, options=None, alias=None):
        """Add additional template engines for configuration on Pylons WSGI
        init.
        
        ``engine``
            The name of the template engine
        
        ``root``
            Template root for the engine
        
        ``options``
            Dict of additional options used during engine initialization, if
            not provided, default to using the template_options dict.
        
        ``alias``
            Name engine should respond to when actually used. This allows for
            multiple configurations of the same engine and lets you alias the
            additional ones to other names.
        
        Example of Kid addition:
        
        .. code-block:: Python
            
            # In yourproj/middleware.py
            # ...
            config.init_app(global_conf, app_conf, package='yourproj')

            # Load additional template engines
            kidopts = {'kid.assume_encoding':'utf-8', 'kid.encoding':'utf-8'}
            config.add_template_engine('kid', 'yourproj.kidtemplates', kidopts)
        
        Example of changing the default template engine:
        
        .. code-block:: Python

            # In yourproj/middleware.py
            # ...
            config.init_app(global_conf, app_conf, package='yourproj')
            
            # Remove existing template engine
            old_default = config.template_engines.pop()
            
            # Load additional template engines
            kidopts = {'kid.assume_encoding':'utf-8', 'kid.encoding':'utf-8'}
            config.add_template_engine('kid', 'yourproj.kidtemplates', kidopts)
            
            # Add old default as additional engine
            config.template_engines.append(old_default)
        """
        if not options:
            options = self.template_options
        config = dict(engine=engine, template_root=root, 
            template_options=options, alias=alias)
        self.template_engines.append(config)
    
    def init_app(self, global_conf, app_conf, package,
                 template_engine='pylonsmyghty'):
        """Initialize configuration for the application
        
        ``global_config``
            Several options are expected to be set for a Pylons web
            application. They will be loaded from the global_config which has
            the main Paste options. If ``debug`` is not enabled as a global
            config option, the following option *must* be set:
            
            * error_to - The email address to send the debug error to
            
            The optional config options in this case are:
            
            * smtp_server - The SMTP server to use, defaults to 'localhost'
            * error_log - A logfile to write the error to
            * error_subject_prefix - The prefix of the error email subject
            * from_address - Whom the error email should be from
        ``app_conf``
            Defaults supplied via the [app:main] section from the Paste
            config file. ``load_config`` only cares about whether a 'prefix'
            option is set, if so it will update Routes to ensure URL's take
            that into account.
        ``package``
            The name of the application package, to be stored in the app_conf.
        ``template_engine``
            Declare the default template engine to setup. Choices are kid,
            genshi, mako, and pylonsmyghty (the default custom Pylons plugin).
        """
        self.global_conf = global_conf
        self.app_conf = app_conf
        self.package = package
        
        app_conf['package'] = package
        
        # Setup the prefix to override the routes if necessary.
        prefix = app_conf.get('prefix')
        if not prefix:
            prefix = global_conf.get('prefix')
        if prefix:
            warnings.warn(pylons.legacy.prefix_warning % prefix,
                          DeprecationWarning, 2)
            self.map.prefix = app_conf['prefix']
            self.map._created_regs = False
        
        errorware = {}
        # Load the errorware configuration from the Paste configuration file
        # These all have defaults, and emails are only sent if configured and
        # if this application is running in production mode
        errorware['debug'] = asbool(global_conf.get('debug'))
        if not errorware['debug']:
            errorware['debug'] = False
            errorware['error_email'] = global_conf.get('email_to')
            errorware['error_log'] = global_conf.get('error_log', None)
            errorware['smtp_server'] = global_conf.get('smtp_server', 
                'localhost')
            errorware['error_subject_prefix'] = global_conf.get(
                'error_subject_prefix', 'WebApp Error: ')
            errorware['from_address'] = global_conf.get('from_address', 
                global_conf.get('error_email_from', 'pylons@yourapp.com'))
            errorware['error_message'] = global_conf.get('error_message', 
                'An internal server error occurred')
        
        # Standard Pylons configuration directives for Myghty
        myghty_defaults = {}
        
        # Raise a complete error for the error middleware to catch
        myghty_defaults['raise_error'] = True
        myghty_defaults['output_encoding'] = self.response_settings['charset']
        myghty_defaults['component_root'] = [{os.path.basename(path): path} \
            for path in self.paths['templates']]
                    
        # Merge in the user-supplied Myghty values
        myghty_defaults.update(self.myghty)
        
        # Merge additional globals
        myghty_defaults.setdefault('allow_globals',
                                   []).extend(pylons.templating.PYLONS_VARS)
        
        self.myghty = myghty_defaults
        myghty_template_options = {}
        if 'myghty_data_dir' in app_conf:
            myghty_defaults['data_dir'] = app_conf['myghty_data_dir']
        elif 'cache_dir' in app_conf:
            myghty_defaults['data_dir'] = os.path.join(app_conf['cache_dir'], 
                'templates')
        
        # Copy Myghty defaults and options into template options
        for k, v in self.myghty.iteritems():
            myghty_template_options['myghty.'+k] = v
            
            # Legacy copy of session and cache settings into app_conf
            if k.startswith('session_') or k.startswith('cache_'):
                self.app_conf[k] = v
            
        
        if 'session_data_dir' not in app_conf:
            app_conf['session_data_dir'] = os.path.join(app_conf['cache_dir'], 
                'sessions')
        if 'cache_data_dir' not in app_conf:
            app_conf['cache_data_dir'] = os.path.join(app_conf['cache_dir'], 
            'cache')

        # Setup the main template options dict
        self.template_options.update(myghty_template_options)
        
        # Setup several defaults for various template languages
        defaults = {}
        
        # Rearrange template options as default for Mako
        defaults['mako.directories'] = self.paths['templates']
        defaults['mako.filesystem_checks'] = True
        defaults['mako.output_encoding'] = \
            self.response_settings['charset']
        if 'cache_dir' in app_conf:
            defaults['mako.module_directory'] = \
                os.path.join(app_conf['cache_dir'], 'templates')
        
        # Setup kid defaults
        defaults['kid.assume_encoding'] = 'utf-8'
        defaults['kid.encoding'] = self.response_settings['charset']
        
        # Merge template options into defaults
        defaults.update(self.template_options)
        self.template_options = defaults

        # Prepare our default template engine
        if template_engine == 'pylonsmyghty':
            self.add_template_engine('pylonsmyghty', None,
                                     myghty_template_options)
        elif template_engine == 'mako':
            self.add_template_engine('mako', '')
        elif template_engine in ['genshi', 'kid']:
            self.add_template_engine(template_engine, package + '.templates')
        
        # Save our errorware values
        self.errorware = errorware

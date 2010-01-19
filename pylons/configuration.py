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
import logging
import os

from paste.config import DispatchingConfig
from paste.deploy.converters import asbool
from webhelpers.mimehelper import MIMETypes


default_template_engine = 'mako'

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

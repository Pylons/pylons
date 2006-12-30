"""Paster Commands, for use with paster in your project

The command(s) listed here are for use with Paste to enable easy creation of
various core Pylons templates.

Currently available commands are::

    controller, shell
"""
import os
import sys
import pylons
import pylons.util as util

from paste.script.command import Command, BadCommand
from paste.script.filemaker import FileOp
from paste.deploy import loadapp, appconfig
import paste.deploy.config
import paste.fixture
import paste.registry

def validate_name(name):
    """Validate that the name for the controller isn't present on the
    path already"""
    if not name:
        # This happens when the name is an existing directory
        raise BadCommand('Please give the name of a controller.')
    try:
        __import__(name)
        raise BadCommand(
            "\n\nA module named '%s' is already present in your "
            "PYTHON_PATH.\n Choosing a conflicting name will likely cause"
            " import problems in\n your controller at some point. It's "
            "suggested that you choose an alternate\nname, and if you'd "
            "like that name to be accessible as '%s', add a route\n"
            "to your projects config/routing.py file similar to:\n"
            "  map.connect('%s', controller='my_%s')" \
            % (name, name, name, name))
    except ImportError:
        # This is actually the result we want
        pass
    
    return True

class ControllerCommand(Command):
    """Create a Controller and accompanying functional test
    
    The Controller command will create the standard controller template
    file and associated functional test to speed creation of controllers.
    
    Example usage::
    
        yourproj% paster controller comments
        Creating yourproj/yourproj/controllers/comments.py
        Creating yourproj/yourproj/tests/functional/test_comments.py
    
    If you'd like to have controllers underneath a directory, just include
    the path as the controller name and the necessary directories will be
    created for you::
    
        yourproj% paster controller admin/trackback
        Creating yourproj/controllers/admin
        Creating yourproj/yourproj/controllers/admin/trackback.py
        Creating yourproj/yourproj/tests/functional/test_admin_trackback.py
    """
    summary = __doc__.splitlines()[0]
    usage = 'CONTROLLER_NAME'
    
    min_args = 1
    max_args = 1
    group_name = 'pylons'
    
    default_verbosity = 3
    
    parser = Command.standard_parser(simulate=True)
    parser.add_option('--no-test',
                      action='store_true',
                      dest='no_test',
                      help="Don't create the test; just the controller")

    def command(self):
        """Main command to create controller"""
        try:
            file_op = FileOp(source_dir=os.path.join(
                os.path.dirname(__file__), 'templates'))
            try:
                name, directory = file_op.parse_path_name_args(self.args[0])
            except:
                raise BadCommand('No egg_info directory was found')
            
            # Check the name isn't the same as the package
            base_package, cdir = file_op.find_dir('controllers', True)
            if base_package.lower() == name.lower():
                raise BadCommand(
                    'Your controller name should not be the same as '
                    'the package name %r.'% base_package
            )
            # Validate the name
            name = name.replace('-', '_')
            validate_name(name)

            # Setup the controller
            fullname = os.path.join(directory, name)
            controller_name = util.class_name_from_module_name(
                name.split('/')[-1])
            if not fullname.startswith(os.sep):
                fullname = os.sep + fullname
            testname = fullname.replace(os.sep, '_')[1:]
            file_op.template_vars.update({'name': controller_name,
                                  'fname': os.path.join(directory, name)})
            file_op.copy_file(template='controller.py_tmpl',
                         dest=os.path.join('controllers', directory), 
                         filename=name)
            if not self.options.no_test:
                file_op.copy_file(template='test_controller.py_tmpl',
                             dest=os.path.join('tests', 'functional'),
                             filename='test_'+testname)
        except BadCommand, e:
            raise BadCommand('An error occurred. %s' % e)
        except:
            msg = str(sys.exc_info()[1])
            raise BadCommand('An unknown error occurred. %s' % msg)

class ShellCommand(Command):
    """Open an interactive shell with the Pylons app loaded
    
    The optional CONFIG_FILE argument specifies the config file to use for
    the interactive shell. CONFIG_FILE defaults to 'development.ini'.
    
    This allows you to test your mapper, models, and simulate web requests
    using ``paste.fixture``.
    
    Example::
        
        $ paster shell my-development.ini
    """
    summary = __doc__.splitlines()[0]
    usage = '[CONFIG_FILE]'
    
    min_args = 0
    max_args = 1
    group_name = 'pylons'
    
    parser = Command.standard_parser(simulate=True)

    def command(self):
        """Main command to create a new shell"""
        self.verbose = 3
        if len(self.args) == 0:
            # Assume the .ini file is ./development.ini
            config_file = 'development.ini'
            if not os.path.isfile(config_file):
                raise BadCommand('%sError: CONFIG_FILE not found at: .%s%s\n'
                                 'Please specify a CONFIG_FILE' % \
                                 (self.parser.get_usage(), os.path.sep,
                                  config_file))
        else:
            config_file = self.args[0]
            
        config_name = 'config:%s' % config_file
        here_dir = os.getcwd()
        locs = dict(__name__="pylons-admin")
        pkg_name = here_dir.split(os.path.sep)[-1].lower()

        # Load app config into paste.deploy to simulate request config
        app_conf = appconfig(config_name, relative_to=here_dir)
        conf = dict(app=app_conf, app_conf=app_conf)
        paste.deploy.config.CONFIG.push_thread_config(conf)
        
        # Load locals and populate with objects for use in shell
        sys.path.insert(0, here_dir)
        
        # Load the wsgi app first so that everything is initialized right
        wsgiapp = loadapp(config_name, relative_to=here_dir)
        test_app = app=paste.fixture.TestApp(wsgiapp)
        
        # Query the test app to setup the environment
        tresponse = test_app.get('/_test_vars')
        request_id = int(tresponse.body)

        # Restore the state of the Pylons special objects
        # (StackedObjectProxies)
        paste.registry.restorer.restoration_begin(request_id)

        # Start the rest of our imports now that the app is loaded
        has_models = True
        try:
            models_package = pkg_name + '.models'
            __import__(models_package)
        except ImportError:
            has_models = False

        # Import all objects from the base module
        try:
            base_module = pkg_name + '.lib.base'
            __import__(base_module)
        except ImportError:
            # Minimal template
            base_module = pkg_name + '.controllers'
            __import__(base_module)
            
        base = sys.modules[base_module]
        base_public = [__name for __name in dir(base) if not \
                       __name.startswith('_') or __name == '_']
        locs.update([(name, getattr(base, name)) for name in base_public])
        locs.update(
            dict(
                mapper=tresponse.pylons_config.map,
                wsgiapp=wsgiapp,
                app=test_app,
            )
        )
        if has_models:
            locs['model'] = sys.modules[models_package],

        banner = "Pylons Interactive Shell\nPython %s\n\n" % sys.version
        banner += "  All objects from %s are available\n" % base_module
        banner += "  Additional Objects:\n"
        banner += "  %-10s -  %s\n" % ('mapper', 'Routes mapper object')
        if has_models:
            banner += "  %-10s -  %s\n" % ('model',
                                           'Models from models package')
        banner += "  %-10s -  %s\n" % ('wsgiapp', 
            'This projects WSGI App instance')
        banner += "  %-10s -  %s\n" % ('app', 
            'paste.fixture wrapped around wsgiapp')

        try:
            # try to use IPython if possible
            import IPython
        
            class CustomIPShell(IPython.iplib.InteractiveShell):
                """Custom shell class to handle raw input"""
                def raw_input(self, *args, **kw):
                    """Capture raw input in exception wrapping"""
                    try:
                        return IPython.iplib.InteractiveShell.raw_input(
                            self, *args, **kw)
                    except EOFError:
                        # In the future, we'll put our own override as needed 
                        # to save models, TG style
                        raise EOFError

            shell = IPython.Shell.IPShell(user_ns=locs, 
                shell_class=CustomIPShell)
            try:
                shell.mainloop()
            finally:
                paste.registry.restorer.restoration_end()
        except ImportError:
            import code
            
            class CustomShell(code.InteractiveConsole):
                """Custom shell class to handle raw input"""
                def raw_input(self, *args, **kw):
                    """Capture raw input in exception wrapping"""
                    try:
                        return code.InteractiveConsole.raw_input(
                            self, *args, **kw)
                    except EOFError:
                        # In the future, we'll put our own override as needed 
                        # to save models, TG style
                        raise EOFError
            
            shell = CustomShell(locals=locs)
            try:
                import readline
            except ImportError:
                pass
            try:
                shell.interact(banner)
            finally:
                paste.registry.restorer.restoration_end()


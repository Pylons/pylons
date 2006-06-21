"""Paster Commands, for use with paster in your project

The command(s) listed here are for use with Paste to enable easy creation of
various core Pylons templates.

Currently available commands are::

    controller, shell
"""
import os
import os.path
import sys
import glob

from paste.script.command import Command, BadCommand
from paste.script.filemaker import FileOp
from paste.script import pluginlib, copydir
from paste.deploy import loadapp, appconfig
import paste.deploy.config
import paste.fixture

class ControllerCommand(Command):
    """Create a Controller and functional test for it
    
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
    summary = __doc__
    usage = 'CONTROLLER_NAME'
    
    min_args = 1
    max_args = 1
    group_name = 'pylons'
    
    parser = Command.standard_parser(simulate=True)
    parser.add_option('--no-test',
                      action='store_true',
                      dest='no_test',
                      help="Don't create the test; just the controller")

    def command(self):
        try:
            self.verbose = 3
            fo = FileOp(source_dir=os.path.join(os.path.dirname(__file__), 'templates'))
            try:
                name, dir = fo.parse_path_name_args(self.args[0])
            except:
                raise BadCommand('No egg_info directory was found')
            fullname = os.path.join(dir, name)
            if not fullname.startswith(os.sep): fullname = os.sep + fullname
            testname = fullname.replace(os.sep, '_')[1:]
            fo.template_vars.update({'name': name.title().replace('-', '_'),
                                  'fullname': fullname,
                                  'fname': os.path.join(dir, name),
                                  'lname': name})
            fo.copy_file(template='controller.py_tmpl',
                         dest=os.path.join('controllers', dir), filename=name)
            if not self.options.no_test:
                fo.copy_file(template='test_controller.py_tmpl',
                             dest=os.path.join('tests', 'functional'),
                             filename='test_'+testname)
        except:
            import sys
            msg = str(sys.exc_info()[1])
            raise BadCommand('An unknown error ocurred, %s' % msg)

class ShellCommand(Command):
    """Open an interactive shell with the Pylons app loaded
    
    The optional CONFIG_FILE argument specifies the config file to use for
    the interactive shell. CONFIG_FILE defaults to 'development.ini'.
    
    This allows you to test your mapper, models, and simulate web requests
    using ``paste.fixture``.
    
    Example::
        
        $ paster shell my-development.ini
    """
    summary = __doc__
    usage = '[CONFIG_FILE]'
    
    min_args = 0
    max_args = 1
    group_name = 'pylons'
    
    parser = Command.standard_parser(simulate=True)

    def command(self):
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
        
        # Start the rest of our imports now that the app is loaded
        routing_package = pkg_name + '.config.routing'
        models_package = pkg_name + '.models'
        helpers_package = pkg_name + '.lib.helpers'
        
        # Import all the modules
        for pack in [routing_package, models_package, helpers_package]:
            __import__(pack)
        
        make_map = getattr(sys.modules[routing_package], 'make_map')
        mapper = make_map()
        
        locs.update(
            dict(
                model=sys.modules[models_package],
                mapper=mapper,
                wsgiapp=wsgiapp,
                app=paste.fixture.TestApp(wsgiapp),
                h=sys.modules[helpers_package],
            )
        )
                
        banner = "Pylons Interactive Shell\nPython %s\n\n" % sys.version
        banner += "Additional Objects:\n"
        banner += "  %-10s -  %s\n" % ('mapper', 'Routes mapper object')
        banner += "  %-10s -  %s\n" % ('h', 'Helper object')
        banner += "  %-10s -  %s\n" % ('model', 'Models from models package')
        banner += "  %-10s -  %s\n" % ('wsgiapp', 'This projects WSGI App instance')
        banner += "  %-10s -  %s\n" % ('app', 'paste.fixture wrapped around wsgiapp')
        try:
            # try to use IPython if possible
            import IPython
        
            class CustomIPShell(IPython.iplib.InteractiveShell):
                def raw_input(self, *args, **kw):
                    try:
                        return IPython.iplib.InteractiveShell.raw_input(self, *args, **kw)
                    except EOFError:
                        # In the future, we'll put our own override as needed to save
                        # models, TG style
                        raise EOFError

            shell = IPython.Shell.IPShell(user_ns=locs, shell_class=CustomIPShell)
            shell.mainloop()
        except ImportError:
            import code
            
            class CustomShell(code.InteractiveConsole):
                def raw_input(self, *args, **kw):
                    try:
                        return code.InteractiveConsole.raw_input(self, *args, **kw)
                    except EOFError:
                        # In the future, we'll put our own override as needed to save
                        # models, TG style
                        raise EOFError
            
            shell = CustomShell(locals=locs)
            shell.interact(banner)

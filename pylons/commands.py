"""Paster Commands, for use with paster in your project

The command(s) listed here are for use with Paste to enable easy creation of
various core Pylons templates.

Currently available commands are::

    controller
"""
import os
import glob
from paste.script.command import Command, BadCommand
from paste.script.filemaker import FileOp
from paste.script import pluginlib, copydir

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
    summary = "Create Controller"
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

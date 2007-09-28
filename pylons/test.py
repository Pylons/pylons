"""Test related functionality"""
import os
import sys

import nose.plugins
import pkg_resources
from paste.deploy import loadapp

class PylonsPlugin(nose.plugins.Plugin):

    """Nose plugin extension

    For use with nose to allow a project to be configured before nose
    proceeds to scan the project for doc tests and unit tests. This
    prevents modules from being loaded without a configured Pylons
    environment.
    """

    enabled = False
    enableOpt = 'pylons_config'
    name = 'pylons'

    def add_options(self, parser, env=os.environ):
        """Add command-line options for this plugin"""
        env_opt = 'NOSE_WITH_%s' % self.name.upper()
        env_opt.replace('-', '_')

        parser.add_option("--with-%s" % self.name,
                          dest=self.enableOpt, type="string",
                          default="",
                          help="Setup Pylons environment with the config file"
                          " specified by ATTR [NOSE_ATTR]")

    def configure(self, options, conf):
        """Configure the plugin"""
        self.config_file = None
        self.conf = conf
        if hasattr(options, self.enableOpt):
            self.enabled = bool(getattr(options, self.enableOpt))
            self.config_file = getattr(options, self.enableOpt)

    def begin(self):
        """Called before any tests are collected or run

        Loads the application, and in turn its configuration.
        """
        path = os.getcwd()
        sys.path.insert(0, path)
        pkg_resources.working_set.add_entry(path)
        self.app = loadapp('config:' + self.config_file, relative_to=path)

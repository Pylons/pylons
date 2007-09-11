"""Nose plugin extension

For use with nose to allow a project to be configured before nose proceeds
to scan the project for doc tests and unit tests. This prevents modules from
being loaded without a configured Pylons environment.

"""
import os

from paste.deploy import loadapp
from nose.plugins import Plugin

class PylonsPlugin(Plugin):
    
    enabled = False
    enableOpt = 'pylons_config'
    name = 'pylons'

    def add_options(self, parser, env=os.environ):
        """Add command-line options for this plugin."""
        env_opt = 'NOSE_WITH_%s' % self.name.upper()
        env_opt.replace('-', '_')
        
        parser.add_option("--with-%s" % self.name,
                          dest=self.enableOpt, type="string",
                          default="",
                          help="Setup Pylons environment with the config file"
                          " specified by ATTR [NOSE_ATTR]")

    def configure(self, options, conf):
        self.config_file = None
        self.conf = conf
        if hasattr(options, self.enableOpt):
            self.enabled = bool(getattr(options, self.enableOpt))
            self.config_file = getattr(options, self.enableOpt)

    def begin(self):
        self.app = loadapp('config:' + self.config_file, relative_to=os.getcwd())

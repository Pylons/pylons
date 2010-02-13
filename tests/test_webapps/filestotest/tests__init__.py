"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
from routes.util import URLGenerator
from webtest import TestApp

import pylons.test

__all__ = ['environ', 'url', 'TestController']

try:
    from sqlalchemy import engine_from_config
    from projectname.model.meta import Session, Base
    from projectname.model import Foo, init_model
    SQLAtesting = True
except:
    SQLAtesting = False

import os
from paste.deploy import appconfig
from projectname.config.environment import load_environment

here_dir = os.path.dirname(__file__)
conf_dir = os.path.dirname(os.path.dirname(here_dir))

test_file = os.path.join(conf_dir, 'test.ini')
conf = appconfig('config:' + test_file)
config = load_environment(conf.global_conf, conf.local_conf)

if SQLAtesting:
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

# Invoke websetup with the current config file
SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

environ = {}

class TestController(TestCase):
    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)
    



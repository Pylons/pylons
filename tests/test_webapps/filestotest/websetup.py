"""Setup the projectname application"""
import logging

import pylons.test

from projectname.config.environment import load_environment
from projectname.model.meta import Session, Base
from projectname.model import Foo
from sqlalchemy import engine_from_config

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup projectname here"""
    config = load_environment(conf.global_conf, conf.local_conf)
    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)

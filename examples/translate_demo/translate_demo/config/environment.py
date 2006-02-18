import sys, os

import pylons.config

from translate_demo.config.routing import map

# Setup our paths
paths = {}
paths['root_path'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths['controllers'] = paths['root_path'] + '/controllers'
paths['templates'] = [paths['root_path'] + '/templates', paths['root_path'] + '/components']
paths['static_files'] = paths['root_path'] + '/public'
[sys.path.append(paths['root_path'] + path) for path in [paths['controllers'], '/lib']]


# The following options are passed directly into Myghty, so all configuration options
# available to the Myghty handler are available for your use here
config = {}
config['session_key'] = 'translate_demo'
config['session_secret'] = 'CHANGEME'

config['log_errors'] = True

# Add your own Myghty config options here, note that all config options will override
# any Pylons config options

load_config = pylons.config.pylons_config(config, map, paths)

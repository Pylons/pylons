import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect

log = logging.getLogger(__name__)

class HelloController(WSGIController):
    def __init__(self):
        self._pylons_log_debug = True

    def index(self):
        return 'Hello World'
    
    def oops(self):
        raise Exception('oops')

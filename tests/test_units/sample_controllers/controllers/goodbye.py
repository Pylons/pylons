import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from webob import Response
from webob.exc import HTTPNotFound

log = logging.getLogger(__name__)

class Smithy(WSGIController):
    def __init__(self):
        self._pylons_log_debug = True

    def index(self):
        return 'Hello World'
    
__controller__ = 'Smithy'

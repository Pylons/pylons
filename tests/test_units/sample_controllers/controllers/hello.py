import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako
from webob import Response
from webob.exc import HTTPNotFound

log = logging.getLogger(__name__)

class HelloController(WSGIController):
    def __init__(self):
        self._pylons_log_debug = True

    def index(self):
        return 'Hello World'
    
    def oops(self):
        raise Exception('oops')
    
    def abort(self):
        abort(404)
    
    def intro_template(self):
        return render_mako('/hello.html')
    
    def time_template(self):
        return render_mako('/time.html', cache_key='fred', cache_expire=20)


def special_controller(environ, start_response):
    return HTTPNotFound()

def empty_wsgi(environ, start_response):
    return

def a_view(request):
    return Response('A View')

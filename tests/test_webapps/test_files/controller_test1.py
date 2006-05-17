from projectname.lib.base import *

class Test1Controller(BaseController):
    def index(self):
        return WSGIResponse('basic index page')
    
    def session_increment(self):
        session.setdefault('counter', -1)
        session['counter'] += 1
        session.save()
        return WSGIResponse('session incrementer')
    
    def globalup(self):
        return WSGIResponse(g.message)
    
    def global_store(self, id):
        if id:
            g.counter += int(id)
        return WSGIResponse(str(g.counter))
    
    def myself(self):
        return WSGIResponse(h.url_for())
    
    def myparams(self):
        return WSGIResponse(str(params))
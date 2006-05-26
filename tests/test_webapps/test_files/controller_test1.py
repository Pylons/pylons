from projectname.lib.base import *

class Test1Controller(BaseController):
    def index(self):
        return response('basic index page')
    
    def session_increment(self):
        session.setdefault('counter', -1)
        session['counter'] += 1
        session.save()
        return response('session incrementer')
    
    def globalup(self):
        return response(g.message)
    
    def global_store(self, id):
        if id:
            g.counter += int(id)
        return response(str(g.counter))
    
    def myself(self):
        return response(h.url_for())
    
    def myparams(self):
        return response(str(params))

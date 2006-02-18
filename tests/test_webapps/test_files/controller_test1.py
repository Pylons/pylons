from projectname.lib.base import *

class Test1Controller(BaseController):
    def index(self):
        m.write('basic index page')
    
    def session_increment(self):
        if not session.has_key('counter'):
            session['counter'] = 0
        else:
            session['counter'] += 1
        session.save()
        m.write('session incrementer')
    
    def globalup(self):
        m.write(g.message)
    
    def global_store(self, id):
        if id:
            g.counter += int(id)
        m.write(str(g.counter))
    
    def myself(self):
        m.write(h.url_for())
    
    def myparams(self):
        m.write(str(params))
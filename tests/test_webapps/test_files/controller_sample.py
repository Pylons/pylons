from projectname.lib.base import *

class SampleController(BaseController):
    def index(self):
        return Response('basic index page')
    
    def session_increment(self):
        session.setdefault('counter', -1)
        session['counter'] += 1
        session.save()
        return Response('session incrementer')
    
    def globalup(self):
        return Response(g.message)
    
    def global_store(self, id):
        if id:
            g.counter += int(id)
        return Response(str(g.counter))
    
    def myself(self):
        return Response(h.url_for())
    
    def myparams(self):
        return Response(str(request.params))
    
    def testdefault(self):
        return render_response('testkid')

    def test_extra_engine(self):
        return render_response('kid', 'testkid')
    
    def test_template_caching(self):
        return render_response('/test_myghty.myt', cache_expire='never')
    
    def test_only_post(self):
        return Response('It was a post!')
    test_only_post = rest.dispatch_on(GET='test_only_get')(rest.restrict('POST')(test_only_post))
    
    def test_only_get(self):
        return Response('It was a get!')
    test_only_get = rest.restrict('GET')(test_only_get)
    
    def impossible(self):
        return Response('This should never be shown')
    impossible = rest.restrict('POST')(rest.dispatch_on(POST='test_only_post')(impossible))

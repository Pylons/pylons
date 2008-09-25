from projectname.tests import *
from xmlrpclib import loads, dumps

class TestXmlrpcController(TestController):
    xmlurl = None
    
    def xmlreq(self, method, args=None):
        if args is None:
            args = ()
        ee = dict(CONTENT_TYPE='text/xml')
        data = dumps(args, methodname=method)
        response = self.app.post(self.xmlurl, params = data, extra_environ=ee)
        return loads(response.body)[0][0]
    
    def setUp(self):
        self.xmlurl = url(controller='xmlrpc')
    
    def test_index(self):
        response = self.xmlreq('userstatus')
        assert response == 'basic string'
    
    def test_structure(self):
        response = self.xmlreq('docs')
        assert dict(mess='a little somethin', a=1, b=[1,2,3], c=['all','the']) == response
        
    def test_methodhelp(self):
        response = self.xmlreq('system.methodHelp', ('docs',))
        assert "This method has a docstring" in response
    
    def test_methodsignature(self):
        response = self.xmlreq('system.methodSignature', ('docs',))
        assert [['struct']] == response
    
    def test_listmethods(self):
        response = self.xmlreq('system.listMethods')
        assert response == ['docs', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'uni', 'userstatus']
    
    def test_unicode(self):
        response = self.xmlreq('uni')
        assert 'A unicode string' in response['mess']
from paste.wsgiwrappers import WSGIRequest
from paste.fixture import TestApp
from paste.registry import RegistryManager

import pylons
from pylons.util import ContextObj
from pylons.controllers import XMLRPCController
import xmlrpclib

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

class BaseXMLRPCController(XMLRPCController):
    def userstatus(self):
        return 'basic string'
    userstatus.signature = [ ['string'] ]
    
    def docs(self):
        "This method has a docstring"
        return dict(mess='a little somethin', a=1, b=[1,2,3], c=('all','the'))
    docs.signature = [ ['struct'] ]

    def uni(self):
        "This method has a docstring"
        return dict(mess=u'A unicode string, oh boy')
    uni.signature = [ ['struct'] ]
    
    def nosig(self):
        return 'not much'
    
    def longdoc(self):
        """This function
        has multiple lines
        in it"""
        return "hi all"

class TestXMLRPCController(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        self.baseenviron['pylons.routes_dict'] = {}
        app = ControllerWrap(BaseXMLRPCController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron, setup_cache=False)
        app = RegistryManager(app)
        self.app = TestApp(app)

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
        assert response == ['docs', 'longdoc', 'nosig', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'uni', 'userstatus']
    
    def test_unicode(self):
        response = self.xmlreq('uni')
        assert 'A unicode string' in response['mess']

    def test_badargs(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'system.methodHelp')

    def test_missingmethod(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'doesntexist')
    
    def test_nosignature(self):
        response = self.xmlreq('system.methodSignature', ('nosig',))
        assert response == ''
    
    def test_nodocs(self):
        response = self.xmlreq('system.methodHelp', ('nosig',))
        assert response == ''
    
    def test_multilinedoc(self):
        response = self.xmlreq('system.methodHelp', ('longdoc',))
        assert 'This function\nhas multiple lines\nin it' in response
        
        
# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

import pylons
from pylons.util import ContextObj
from pylons.controllers import XMLRPCController
import xmlrpclib

from __init__ import TestWSGIController, SetupCacheGlobal, ControllerWrap

class BaseXMLRPCController(XMLRPCController):
    foo = 'bar'
    
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
    
    def intargcheck(self, arg):
        if not isinstance(arg, int):
            return xmlrpclib.Fault(0, 'Integer required')
        else:
            return "received int"
    intargcheck.signature = [ ['string', 'int'] ]
    
    def nosig(self):
        return 'not much'
    
    def structured_methodname(self, arg):
        "This method has a docstring"
        return 'Transform okay'
    structured_methodname.signature = [ ['string', 'string'] ]
    
    def longdoc(self):
        """This function
        has multiple lines
        in it"""
        return "hi all"
    
    def _private(self):
        return 'private method'
    
class TestXMLRPCController(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        self.baseenviron['pylons.routes_dict'] = {}
        app = ControllerWrap(BaseXMLRPCController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
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
    
    def test_methodhelp_with_structured_methodname(self):
        response = self.xmlreq('system.methodHelp', ('structured.methodname',))
        assert "This method has a docstring" in response
    
    def test_methodsignature(self):
        response = self.xmlreq('system.methodSignature', ('docs',))
        assert [['struct']] == response
    
    def test_methodsignature_with_structured_methodname(self):
        response = self.xmlreq('system.methodSignature', ('structured.methodname',))
        assert [['string', 'string']] == response
    
    def test_listmethods(self):
        response = self.xmlreq('system.listMethods')
        assert response == ['docs', 'intargcheck', 'longdoc', 'nosig', 'structured.methodname', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'uni', 'userstatus']    
    
    def test_unicode(self):
        response = self.xmlreq('uni')
        assert 'A unicode string' in response['mess']
    
    def test_unicode_method(self):
        data = xmlrpclib.dumps((), methodname=u'ОбсуждениеКомпаний')
        self.response = response = self.app.post('/', params=data, extra_environ=dict(CONTENT_TYPE='text/xml'))
    
    def test_badargs(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'system.methodHelp')
    
    def test_badarity(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'system.methodHelp')
    
    # Unsure whether this is actually picked up by xmlrpclib, but what the hey
    def test_bad_paramval(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'intargcheck', (12.5,))
    
    def test_missingmethod(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'doesntexist')
    
    def test_nosignature(self):
        response = self.xmlreq('system.methodSignature', ('nosig',))
        assert response == ''
    
    def test_nosignature_unicode(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'system.methodSignature',
                          (u'ОбсуждениеКомпаний',))
    
    def test_nodocs(self):
        response = self.xmlreq('system.methodHelp', ('nosig',))
        assert response == ''
    
    def test_nodocs_unicode(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'system.methodHelp',
                          (u'ОбсуждениеКомпаний',))
    
    def test_multilinedoc(self):
        response = self.xmlreq('system.methodHelp', ('longdoc',))
        assert 'This function\nhas multiple lines\nin it' in response
    
    def test_contenttype(self):
        response = self.xmlreq('system.methodHelp', ('longdoc',))
        assert self.response.header('Content-Type') == 'text/xml'
    
    def test_start_response(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'start_response')
    
    def test_private_func(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, '_private')
    
    def test_var(self):
        self.assertRaises(xmlrpclib.Fault, self.xmlreq, 'foo')
    


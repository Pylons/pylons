from projectname.lib.base import *
from pylons.controllers import XMLRPCController

class XmlrpcController(XMLRPCController):
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
    docs.signature = [ ['struct'] ]
    
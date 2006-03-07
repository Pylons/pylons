"""Base objects to be exported for use in Controllers"""

from pylons.controllers import Controller, RPCController
from pylons.decorators import jsonify
from pylons.helpers import SessionProxy, RequestProxy, MyghtyProxy, GlobalsProxy, RequestArgProxy
from pylons.util import RequestLocal, Buffet, Helpers

m = MyghtyProxy()
c = RequestLocal()
g = GlobalsProxy()
session = SessionProxy()
request = RequestProxy()
buffet = Buffet()
params = RequestArgProxy()
h = Helpers(m=m, c=c, session=session, request=request, buffet=buffet)

__all__ = ['Controller', 'RPCController', 'jsonify']

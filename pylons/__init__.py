"""Base objects to be exported for use in Controllers"""

from paste.registry import StackedObjectProxy
from paste.wsgiwrappers import WSGIResponse as Response

from pylons.controllers import Controller, WSGIController, RPCController
from pylons.decorators import jsonify
from pylons.util import Helpers

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")
cache = StackedObjectProxy(name="Cache")
session = StackedObjectProxy(name="Session")
request = StackedObjectProxy(name="Request")
response = Response
buffet = StackedObjectProxy(name="Buffet")
h = Helpers(c=c, session=session, request=request, buffet=buffet)

# Legacy objects
m = StackedObjectProxy(name="m legacy object")
params = StackedObjectProxy(name="params")

__all__ = ['Controller', 'RPCController', 'jsonify']

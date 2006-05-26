"""Base objects to be exported for use in Controllers"""

from paste.registry import StackedObjectProxy
from paste.wsgiwrappers import WSGIResponse as Response

from pylons.controllers import Controller, RPCController
from pylons.decorators import jsonify
from pylons.util import Helpers

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")
cache = StackedObjectProxy(name="Cache")
session = StackedObjectProxy(name="Session")
request = StackedObjectProxy(name="Request")
buffet = StackedObjectProxy(name="Buffet")
params = StackedObjectProxy(name="params")
h = Helpers(c=c, session=session, request=request, buffet=buffet)

# Legacy objects
m = StackedObjectProxy(name="m legacy object")

__all__ = ['Controller', 'RPCController', 'jsonify']

"""Base objects to be exported for use in Controllers"""

from paste.registry import StackedObjectProxy

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
response = StackedObjectProxy(name="response")
h = Helpers(c=c, session=session, request=request, buffet=buffet)

__all__ = ['Controller', 'RPCController', 'jsonify']

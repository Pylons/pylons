"""Base objects to be exported for use in Controllers"""
from paste.registry import StackedObjectProxy
from paste.wsgiwrappers import WSGIResponse as Response

from pylons.controllers import Controller, RPCController
from pylons.decorators import jsonify
from pylons.legacy import m, params

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")
cache = StackedObjectProxy(name="Cache")
session = StackedObjectProxy(name="Session")
request = StackedObjectProxy(name="Request")
buffet = StackedObjectProxy(name="Buffet")
h = StackedObjectProxy(name="h")

translator = StackedObjectProxy(name="Translator")

__all__ = ['Controller', 'RPCController', 'Response', 'jsonify']

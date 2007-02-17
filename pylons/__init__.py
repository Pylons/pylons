"""Base objects to be exported for use in Controllers"""
from paste.registry import StackedObjectProxy
from paste.wsgiwrappers import WSGIResponse as Response

from pylons.legacy import Controller, h, jsonify

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")

cache = StackedObjectProxy(name="Cache")
request = StackedObjectProxy(name="Request")
session = StackedObjectProxy(name="Session")

buffet = StackedObjectProxy(name="Buffet")
translator = StackedObjectProxy(name="Translator")

__all__ = ['c', 'g', 'cache', 'request', 'session', 'jsonify', 'Controller',
           'Response']

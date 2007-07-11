"""Base objects to be exported for use in Controllers"""
from paste.registry import StackedObjectProxy

from pylons.config import config
from pylons.legacy import h, jsonify, Controller, Response

__all__ = ['c', 'g', 'cache', 'request', 'response', 'session', 'jsonify',
           'Controller', 'Response']

c = StackedObjectProxy(name="C")
g = StackedObjectProxy(name="G")

cache = StackedObjectProxy(name="Cache")
request = StackedObjectProxy(name="Request")
response = StackedObjectProxy(name="Response")
session = StackedObjectProxy(name="Session")

buffet = StackedObjectProxy(name="Buffet")
translator = StackedObjectProxy(name="Translator")

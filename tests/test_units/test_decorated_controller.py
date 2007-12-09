# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

import pylons
from pylons.controllers import DecoratedController
from pylons.decorators import expose
from pylons.testutil import ControllerWrap, SetupCacheGlobal
from turbojson.jsonify import jsonify

from __init__ import TestWSGIController

pylons.buffet = pylons.templating.Buffet(default_engine='genshi')

class MyClass(object):
    pass


@jsonify.when('isinstance(obj, MyClass)')
def jsonify_myclass(obj):
    return {'result':'wo-hoo!'}


class BasicDecoratedController(DecoratedController):

    def json(self):
        return dict(a='hello world', b=True)
    json = expose('json')(json)

    def excluded_b(self):
        return dict(a="visible", b="invisible")
    excluded_b = expose('json', exclude_names=["b"])(excluded_b)

    def custom(self):
        return dict(custom=MyClass())
    custom = expose('json')(custom)

    def xml_or_json(self):
        return dict(name="John Carter", title='officer', status='missing')
    xml_or_json = expose('json')(
        expose('xml', content_type='application/xml')(xml_or_json))


class TestDecoratedController(TestWSGIController):
    def __init__(self, *args, **kargs):
        TestWSGIController.__init__(self, *args, **kargs)
        self.baseenviron = {}
        app = ControllerWrap(BasicDecoratedController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)


    def setUp(self):
        TestWSGIController.setUp(self)
        self.baseenviron.update(self.environ)

    def test_simple_jsonification(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'json'
        resp = self.app.get('/json')
        assert '{"a": "hello world", "b": true}' in resp.body

    def test_custom_jsonification(self):
        self.baseenviron['pylons.routes_dict']['action'] = 'custom'
        resp = self.app.get('/custom')
        assert "wo-hoo!" in resp.body

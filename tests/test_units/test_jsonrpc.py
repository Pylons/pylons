# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

import webob.exc as exc
import json

from __init__ import TestWSGIController

def make_basejsonrpc():
    from pylons.controllers import JSONRPCController, JSONRPCError

    class BaseJSONRPCController(JSONRPCController):

        def __init__(self):
            self._pylons_log_debug = True

        def echo(self, message):
            return message

        def int_arg_check(self, arg):
            if not isinstance(arg, int):
                raise JSONRPCError('That is not an integer')
            else:
                return 'got an integer'

        def return_garbage(self):
            return JSONRPCController

        def _private(self):
            return 'private method'

    return BaseJSONRPCController


class TestJSONRPCController(TestWSGIController):

    def __init__(self, *args, **kwargs):
        from pylons.testutil import ControllerWrap, SetupCacheGlobal

        BaseJSONRPCController = make_basejsonrpc()
        TestWSGIController.__init__(self, *args, **kwargs)
        self.baseenviron = {}
        self.baseenviron['pylons.routes_dict'] = {}
        app = ControllerWrap(BaseJSONRPCController)
        app = self.sap = SetupCacheGlobal(app, self.baseenviron)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_echo(self):
        response = self.jsonreq('echo', args=('hello, world',))
        assert dict(id='test',
                    result='hello, world',
                    error=None) == response

    def test_int_arg_check(self):
        response = self.jsonreq('int_arg_check', args=('1',))
        assert dict(id='test',
                    result=None,
                    error='That is not an integer') == response

    def test_return_garbage(self):
        response = self.jsonreq('return_garbage')
        assert dict(id='test',
                    result=None,
                    error='Error encoding response') == response

    def test_private_method(self):
        response = self.jsonreq('_private')
        assert dict(id='test',
                    result=None,
                    error='Method not allowed') == response

    def test_content_type(self):
        response = self.jsonreq('echo', args=('foo',))
        assert self.response.header('Content-Type') == 'application/json'

    def test_missing_method(self):
        response = self.jsonreq('foo')
        assert dict(id='test',
                    result=None,
                    error='No such method: foo') == response

    def test_no_content_length(self):
        data = json.dumps(dict(id='test',
                               method='echo',
                               args=('foo',)))
        self.assertRaises(exc.HTTPLengthRequired,
                          lambda: self.app.post('/', extra_environ=\
                                                    dict(CONTENT_LENGTH='')))

    def test_zero_content_length(self):
        data = json.dumps(dict(id='test',
                               method='echo',
                               args=('foo',)))
        self.assertRaises(exc.HTTPLengthRequired,
                          lambda: self.app.post('/', extra_environ=\
                                                    dict(CONTENT_LENGTH='0')))

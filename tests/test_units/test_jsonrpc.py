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
                raise JSONRPCError(1, 'That is not an integer')
            else:
                return 'got an integer'

        def return_garbage(self):
            return JSONRPCController

        def subtract(self, x, y):
            if not isinstance(x, int) and not isinstance(y, int):
                raise JSONRPCError(1, 'That is not an integer')
            else:
                return x - y

        def v2_echo(self, message='Default message'):
            return message

        def v2_int_arg_check(self, arg=99):
            if not isinstance(arg, int):
                raise JSONRPCError(1, 'That is not an integer')
            else:
                return 'got an integer'

        def v2_decrement(self, x, y=1):
            """Like subtract, but decrements by default."""
            if not isinstance(x, int) and not isinstance(y, int):
                raise JSONRPCError(1, 'That is not an integer')
            else:
                return x - y

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
        assert dict(jsonrpc='2.0',
                    id='test',
                    result='hello, world') == response

    def test_int_arg_check(self):
        response = self.jsonreq('int_arg_check', args=('1',))
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': 1,
                           'message': 'That is not an integer'}) == response

    def test_return_garbage(self):
        response = self.jsonreq('return_garbage')
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': -32603,
                           'message': "Internal error"}) == response

    def test_private_method(self):
        response = self.jsonreq('_private')
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': -32601,
                           'message': "Method not found"}) == response

    def test_content_type(self):
        response = self.jsonreq('echo', args=('foo',))
        assert self.response.header('Content-Type') == 'application/json'

    def test_missing_method(self):
        response = self.jsonreq('foo')
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': -32601,
                           'message': "Method not found"}) == response

    def test_no_content_length(self):
        data = json.dumps(dict(jsonrpc='2.0',
                               id='test',
                               method='echo',
                               args=('foo',)))
        self.assertRaises(exc.HTTPLengthRequired,
                          lambda: self.app.post('/', extra_environ=\
                                                    dict(CONTENT_LENGTH='')))

    def test_zero_content_length(self):
        data = json.dumps(dict(jsonrpc='2.0',
                               id='test',
                               method='echo',
                               args=('foo',)))
        self.assertRaises(exc.HTTPLengthRequired,
                          lambda: self.app.post('/', extra_environ=\
                                                    dict(CONTENT_LENGTH='0')))

    def test_positional_params(self):
        response = self.jsonreq('subtract', args=[4, 2])
        assert dict(jsonrpc='2.0',
                    id='test',
                    result=2) == response

    def test_missing_positional_param(self):
        response = self.jsonreq('subtract', args=[1])
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': -32602,
                           'message': "Invalid params"}) == response

    def test_wrong_param_type(self):
        response = self.jsonreq('subtract', args=['1', '2'])
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': 1,
                           'message': "That is not an integer"}) == response

    def test_v2_echo(self):
        response = self.jsonreq('v2_echo', args={'message': 'hello, world'})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result='hello, world') == response

    def test_v2_echo_default(self):
        response = self.jsonreq('v2_echo', args={})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result='Default message') == response

    def test_v2_int_arg_check_valid(self):
        response = self.jsonreq('v2_int_arg_check', args={'arg': 5})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result='got an integer')

    def test_v2_int_arg_check_default_keyword_argument(self):
        response = self.jsonreq('v2_int_arg_check', args={})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result='got an integer')

    def test_v2_int_arg_check(self):
        response = self.jsonreq('v2_int_arg_check', args={'arg': 'abc'})
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': 1,
                           'message': "That is not an integer"}) == response

    def test_v2_decrement(self):
        response = self.jsonreq('v2_decrement', args={'x': 50, 'y': 100})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result=-50) == response

    def test_v2_decrement_default_keywoard_argument(self):
        response = self.jsonreq('v2_decrement', args={'x': 50})
        assert dict(jsonrpc='2.0',
                    id='test',
                    result=49) == response

    def test_v2_decrement_missing_keyword_argument(self):
        response = self.jsonreq('v2_decrement', args={})
        assert dict(jsonrpc='2.0',
                    id='test',
                    error={'code': -32602,
                           'message': "Invalid params"}) == response

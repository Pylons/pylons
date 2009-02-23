# -*- coding: utf-8 -*-
from webtest import TestApp

from pylons.middleware import StatusCodeRedirect, ErrorHandler

def simple_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['Hello world!']

def simple_exception_app(environ, start_response):
    if environ['PATH_INFO'].startswith('/error/document'):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['Made it to the error']
    else:
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return ['No page found!']

def test_plain_wrap():
    app = TestApp(StatusCodeRedirect(simple_app))
    res = app.get('/')
    assert res.status_int == 200

def test_status_intercept():
    app = TestApp(StatusCodeRedirect(simple_exception_app))
    res = app.get('/', status=404)
    assert 'Made it to the error' in res

def test_original_path():
    app = TestApp(StatusCodeRedirect(simple_exception_app))
    res = app.get('/', status=404)
    assert res.environ['PATH_INFO'] == '/'

def test_retains_response():
    app = TestApp(StatusCodeRedirect(simple_exception_app))
    res = app.get('/', status=404)
    assert 'pylons.original_response' in res.environ
    assert 'No page found!' in res.environ['pylons.original_response'].body

def test_retains_request():
    app = TestApp(StatusCodeRedirect(simple_exception_app))
    res = app.get('/fredrick', status=404)
    assert 'pylons.original_request' in res.environ
    assert '/fredrick' == res.environ['pylons.original_request'].path_info
    
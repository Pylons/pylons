import unittest

from repoze.bfg.testing import cleanUp


class TestRouteUrl(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()
        
    def _callFUT(self, *arg, **kw):
        from pylons.url import route_url
        return route_url(*arg, **kw)

    def test_with_elements(self):
        from repoze.bfg.interfaces import IRoutesMapper
        request = _makeRequest()
        mapper = DummyRoutesMapper(result='/1/2/3')
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = self._callFUT('flub', request, 'extra1', 'extra2',
                               a=1, b=2, c=3, _query={'a':1},
                               _anchor=u"foo")
        self.assertEqual(result,
                         'http://example.com:5432/1/2/3/extra1/extra2?a=1#foo')

    def test_no_elements(self):
        from repoze.bfg.interfaces import IRoutesMapper
        request = _makeRequest()
        mapper = DummyRoutesMapper(result='/1/2/3')
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = self._callFUT('flub', request, a=1, b=2, c=3, _query={'a':1},
                               _anchor=u"foo")
        self.assertEqual(result,
                         'http://example.com:5432/1/2/3?a=1#foo')

    def test_it_generation_error(self):
        from repoze.bfg.interfaces import IRoutesMapper
        request = _makeRequest()
        mapper = DummyRoutesMapper(raise_exc=KeyError)
        request.registry.registerUtility(mapper, IRoutesMapper)
        mapper.raise_exc = KeyError
        self.assertRaises(KeyError, self._callFUT, 'flub', request, a=1)

    def test_generate_doesnt_receive_query_or_anchor(self):
        from repoze.bfg.interfaces import IRoutesMapper
        mapper = DummyRoutesMapper(result='')
        from zope.component import getSiteManager
        sm = getSiteManager()
        sm.registerUtility(mapper, IRoutesMapper)
        request = DummyRequest()
        result = self._callFUT('flub', request, _query=dict(name='some_name'))
        self.assertEqual(mapper.kw, {}) # shouldnt have anchor/query
        self.assertEqual(result, 'http://example.com:5432?name=some_name')

    def test_with_app_url(self):
        from repoze.bfg.interfaces import IRoutesMapper
        request = _makeRequest()
        mapper = DummyRoutesMapper(result='/1/2/3')
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = self._callFUT('flub', request, _app_url='http://example2.com')
        self.assertEqual(result,  'http://example2.com/1/2/3')
    
    def test_custom_url_gen(self):
        from repoze.bfg.interfaces import IRoutesMapper
        request = _makeRequest()
        mapper = DummyRoutesMapper(result='/smith', routes={'flub': DummyRoute})
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = self._callFUT('flub', request, a=1, b=2, c=3, _query={'a':1})
        self.assertEqual(result, 'http://example.com:5432/smith')
        


class DummyRequest:
    application_url = 'http://example.com:5432' # app_url never ends with slash
    def __init__(self, environ=None):
        if environ is None:
            environ = {}
        self.environ = environ

class DummyRoutesMapper:
    raise_exc = None
    def __init__(self, result='/1/2/3', raise_exc=False, routes={}):
        self.result = result
        self.routes = routes

    def generate(self, *route_args, **kw):
        self.kw = kw
        if self.raise_exc:
            raise self.raise_exc
        return self.result

class DummyRoute:
    @staticmethod
    def custom_url_generator(route_name, request, *elements, **kw):
        return route_name, request, [], {}


def _makeRequest(environ=None):
    from repoze.bfg.registry import Registry
    request = DummyRequest(environ)
    request.registry = Registry()
    return request

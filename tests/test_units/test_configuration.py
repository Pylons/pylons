import unittest

class TestConfigurator(unittest.TestCase):
    def _getTargetClass(self):
        from pylons.configuration import Configurator
        return Configurator

    def _assertRoute(self, config, name, path, num_predicates=0):
        from repoze.bfg.interfaces import IRoutesMapper
        mapper = config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        route = routes[0]
        self.assertEqual(len(routes), 1)
        self.assertEqual(route.name, name)
        self.assertEqual(route.path, path)
        self.assertEqual(len(routes[0].predicates), num_predicates)
        return route

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def test_add_route_squiggly_syntax(self):
        config = self._makeOne()
        config.add_route('name', '/abc/{def}/:ghi/jkl/{mno}{/:p')
        self._assertRoute(config, 'name', '/abc/:def/:ghi/jkl/:mno{/:p', 0)
        
    def test_kwargs_passed(self):
        config = self._makeOne()
        config.add_route('name', '/abc', xhr=True)
        self._assertRoute(config, 'name', '/abc', 1)
        

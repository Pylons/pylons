import unittest

class TestConfigurator(unittest.TestCase):
    def _getTargetClass(self):
        from pylons.configuration import Configurator
        return Configurator

    def _assertRoute(self, config, name, path, num_predicates=0, num_routes=1):
        from repoze.bfg.interfaces import IRoutesMapper
        mapper = config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        route = routes[0]
        self.assertEqual(len(routes), num_routes)
        self.assertEqual(route.name, name)
        self.assertEqual(route.path, path)
        self.assertEqual(len(routes[0].predicates), num_predicates)
        return route

    def _makeOne(self, *arg, **kw):
        return self._getTargetClass()(*arg, **kw)

    def test_ctor(self):
        from repoze.bfg.interfaces import IRendererFactory
        config = self._makeOne()
        from repoze.bfg.mako import renderer_factory
        self.assertEqual(config.registry.getUtility(IRendererFactory, '.mak'),
                         renderer_factory)
        self.assertEqual(config.registry.getUtility(IRendererFactory, '.mako'),
                         renderer_factory)
        

    def test_add_route_squiggly_syntax(self):
        config = self._makeOne()
        config.add_route('name', '/abc/{def}/:ghi/jkl/{mno}{/:p')
        self._assertRoute(config, 'name', '/abc/:def/:ghi/jkl/:mno{/:p', 0)
        
    def test_add_route_kwargs_passed(self):
        config = self._makeOne()
        config.add_route('name', '/abc', xhr=True)
        self._assertRoute(config, 'name', '/abc', 1)

    def test_add_handler_action_in_route_pattern(self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        config.add_handler('name', '/{action}', DummyHandler)
        self._assertRoute(config, 'name', '/:action', 0)
        self.assertEqual(len(views), 2)

        view = views[0]
        preds = view['custom_predicates']
        self.assertEqual(len(preds), 1)
        pred = preds[0]
        request = Dummy()
        self.assertEqual(pred(None, request), False)
        request.matchdict = {'action':'action1'}
        self.assertEqual(pred(None, request), True)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['attr'], 'action1')
        self.assertEqual(view['view'], DummyHandler)

        view = views[1]
        preds = view['custom_predicates']
        self.assertEqual(len(preds), 1)
        pred = preds[0]
        request = Dummy()
        self.assertEqual(pred(None, request), False)
        request.matchdict = {'action':'action2'}
        self.assertEqual(pred(None, request), True)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['attr'], 'action2')
        self.assertEqual(view['view'], DummyHandler)

    def test_add_handler_with_view_overridden_autoexpose_None(self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(DummyHandler):
            __autoexpose__ = None
        config.add_handler('name', '/{action}', MyView)
        self._assertRoute(config, 'name', '/:action', 0)
        self.assertEqual(len(views), 0)

    def test_add_handler_with_view_overridden_autoexpose_broken_regex1(self):
        from repoze.bfg.exceptions import ConfigurationError
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(DummyHandler):
            __autoexpose__ = 1
        self.assertRaises(ConfigurationError, config.add_handler,
                          'name', '/{action}', MyView)

    def test_add_handler_with_view_overridden_autoexpose_broken_regex2(self):
        from repoze.bfg.exceptions import ConfigurationError
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(DummyHandler):
            __autoexpose__ = 'a\\'
        self.assertRaises(ConfigurationError, config.add_handler,
                          'name', '/{action}', MyView)

    def test_add_handler_with_view_method_has_expose_config(self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(object):
            def action(self):
                return 'response'
            action.__exposed__ = [{'custom_predicates':(1,)}]
        config.add_handler('name', '/{action}', MyView)
        self._assertRoute(config, 'name', '/:action', 0)
        self.assertEqual(len(views), 1)
        view = views[0]
        preds = view['custom_predicates']
        self.assertEqual(len(preds), 2)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['attr'], 'action')
        self.assertEqual(view['view'], MyView)

    def test_add_handler_with_view_method_has_expose_config_with_action(self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(object):
            def action(self):
                return 'response'
            action.__exposed__ = [{'name':'action3000'}]
        config.add_handler('name', '/{action}', MyView)
        self._assertRoute(config, 'name', '/:action', 0)
        self.assertEqual(len(views), 1)
        view = views[0]
        preds = view['custom_predicates']
        self.assertEqual(len(preds), 1)
        pred = preds[0]
        request = Dummy()
        self.assertEqual(pred(None, request), False)
        request.matchdict = {'action':'action3000'}
        self.assertEqual(pred(None, request), True)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['attr'], 'action')
        self.assertEqual(view['view'], MyView)

    def test_add_handler_with_view_method_has_expose_config_with_action_regex(
        self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        class MyView(object):
            def action(self):
                return 'response'
            action.__exposed__ = [{'name':'^action3000$'}]
        config.add_handler('name', '/{action}', MyView)
        self._assertRoute(config, 'name', '/:action', 0)
        self.assertEqual(len(views), 1)
        view = views[0]
        preds = view['custom_predicates']
        self.assertEqual(len(preds), 1)
        pred = preds[0]
        request = Dummy()
        self.assertEqual(pred(None, request), False)
        request.matchdict = {'action':'action3000'}
        self.assertEqual(pred(None, request), True)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['attr'], 'action')
        self.assertEqual(view['view'], MyView)

    def test_add_handler_doesnt_mutate_expose_dict(self):
        config = self._makeOne()
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        exposed = [{'name':'^action3000$'}]
        class MyView(object):
            def action(self):
                return 'response'
            action.__exposed__ = exposed
        config.add_handler('name', '/{action}', MyView)
        self.assertEqual(exposed[0], {'name':'^action3000$'}) # not mutated

    def test_add_handler_with_action_and_action_in_path(self):
        from repoze.bfg.exceptions import ConfigurationError
        config = self._makeOne()
        self.assertRaises(ConfigurationError, config.add_handler, 
                          'name', '/{action}', DummyHandler, action='abc')

    def test_with_explicit_action(self):
        config = self._makeOne()
        class DummyHandler(object):
            def index(self): pass
            index.__exposed__ = [{'a':'1'}]
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        config.add_handler('name', '/abc', DummyHandler, action='index')
        self.assertEqual(len(views), 1)
        view = views[0]
        self.assertEqual(view['a'], '1')
        self.assertEqual(view['attr'], 'index')
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['view'], DummyHandler)

    def test_with_implicit_action(self):
        config = self._makeOne()
        class DummyHandler(object):
            def __call__(self): pass
            __call__.__exposed__ = [{'a':'1'}]
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        config.add_handler('name', '/abc', DummyHandler)
        self.assertEqual(len(views), 1)
        view = views[0]
        self.assertEqual(view['a'], '1')
        self.assertEqual(view['attr'], None)
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['view'], DummyHandler)
    
    def test_with_multiple_action(self):
        config = self._makeOne()
        class DummyHandler(object):
            def index(self): pass
            def create(self): pass
            create.__exposed__ = [{'name': 'index'}]
        views = []
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        config.add_handler('name', '/abc', DummyHandler, action='index')
        self.assertEqual(len(views), 2)
        view = views[0]
        self.assertEqual(view['attr'], 'create')
        self.assertEqual(view['route_name'], 'name')
        self.assertEqual(view['view'], DummyHandler)
        view = views[1]
        self.assertEqual(view['attr'], 'index')

    def test_string_handler(self):
        import pylons
        views = []
        config = self._makeOne()
        def dummy_add_view(**kw):
            views.append(kw)
        config.add_view = dummy_add_view
        config.add_handler('name', '/abc', 'pylons')
        self.assertEqual(len(views), 1)
        view = views[0]
        self.assertEqual(view['view'], pylons)

    def test_add_helpers_string(self):
        import pylons
        config = self._makeOne()
        config.add_helpers('pylons')
        self.assertEqual(config.registry.helpers, pylons)
        
    def test_add_helpers_notstring(self):
        import pylons
        config = self._makeOne()
        config.add_helpers(pylons)
        self.assertEqual(config.registry.helpers, pylons)

    def test_add_rest_handler(self):
        from repoze.bfg.testing import DummyRequest
        from repoze.bfg.interfaces import IRoutesMapper
        config = self._makeOne()
        hdlr = config.add_rest_handler('messages', 'message', DummyRestHandler)
        mapper = config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 7)
        self.assertEqual(routes[0].name, 'messages')
        self.assertEqual(routes[0].path, 'messages')
        self.assertEqual(len(routes[0].predicates), 1)
        self.assertEqual(routes[1].name, 'messages_create')
        self.assertEqual(routes[1].path, 'messages')
        self.assertEqual(len(routes[1].predicates), 1)
        self.assertEqual(routes[2].name, 'new_message')
        self.assertEqual(routes[2].path, 'messages/new')
        self.assertEqual(len(routes[2].predicates), 1)
        self.assertEqual(routes[3].name, 'message')
        self.assertEqual(routes[3].path, 'messages/:id')
        self.assertEqual(len(routes[3].predicates), 1)
        self.assertEqual(routes[4].name, 'message_update')
        self.assertEqual(routes[4].path, 'messages/:id')
        self.assertEqual(len(routes[4].predicates), 1)
        self.assertEqual(routes[5].name, 'message_delete')
        self.assertEqual(routes[5].path, 'messages/:id')
        self.assertEqual(len(routes[5].predicates), 1)
        self.assertEqual(routes[6].name, 'edit_message')
        self.assertEqual(routes[6].path, 'messages/:id/edit')
        self.assertEqual(len(routes[6].predicates), 1)
        request = DummyRequest()
        request.matchdict = {'id':1}
        handler = hdlr(request)
        self.assertEqual(handler.index(), 'index')
        self.assertEqual(handler.create(), 'create')
        self.assertEqual(handler.new(), 'new')
        self.assertEqual(handler.update(), 1)
        self.assertEqual(handler.delete(), 1)
        self.assertEqual(handler.show(), 1)
        self.assertEqual(handler.edit(), 1)

    def test_add_rest_handler_dottedname(self):
        import pylons
        config = self._makeOne()
        hdlr = config.add_rest_handler('messages', 'message', 'pylons')
        self.assertEqual(hdlr.factory, pylons)

class TestConfiguratorGlobals(unittest.TestCase):
    def setUp(self):
        from pylons.configuration import Configurator
        self.config = Configurator()
        self.config.begin()

    def test_add_globals(self):
        import pylons
        from pylons.configuration import globals_factory
        config = self.config
        req = Dummy()
        req.tmpl_context = Dummy()
        req.registry = config.registry
        sys = {'request': None}
        config.add_helpers(pylons)
        
        result = globals_factory(sys)
        assert pylons == result['h']
        
        sys = {'request': req}
        result = globals_factory(sys)
        assert pylons == result['h']
        assert result['tmpl_context'] == req.tmpl_context
        assert 'session' not in result
        
        req.session = Dummy()
        sys = {'request': req}
        result = globals_factory(sys)
        assert result['session'] == req.session
    
    def tearDown(self):
        self.config.end()


class TestActionPredicate(unittest.TestCase):
    def _getTargetClass(self):
        from pylons.configuration import ActionPredicate
        return ActionPredicate
    
    def _makeOne(self, action='myaction'):
        return self._getTargetClass()(action)

    def test_bad_action_regex_string(self):
        from repoze.bfg.exceptions import ConfigurationError
        cls = self._getTargetClass()
        self.assertRaises(ConfigurationError, cls, '[a-z')

    def test_bad_action_regex_None(self):
        from repoze.bfg.exceptions import ConfigurationError
        cls = self._getTargetClass()
        self.assertRaises(ConfigurationError, cls, None)

    def test___call__no_matchdict(self):
        pred = self._makeOne()
        request = Dummy()
        self.assertEqual(pred(None, request), False)

    def test___call__no_action_in_matchdict(self):
        pred = self._makeOne()
        request = Dummy()
        request.matchdict = {}
        self.assertEqual(pred(None, request), False)

    def test___call__action_does_not_match(self):
        pred = self._makeOne()
        request = Dummy()
        request.matchdict = {'action':'notmyaction'}
        self.assertEqual(pred(None, request), False)

    def test___call__action_matches(self):
        pred = self._makeOne()
        request = Dummy()
        request.matchdict = {'action':'myaction'}
        self.assertEqual(pred(None, request), True)

class Dummy(object):
    pass
            
        
class DummyHandler(object):
    def __init__(self, request):
        self.request = request

    def action1(self):
        return 'response 1'

    def action2(self):
        return 'response 2'

class DummyRestHandler(object):
    def __init__(self, request):
        self.request = request
        
    def index(self):
        return 'index'

    def create(self):
        return 'create'

    def new(self):
        return 'new'

    def update(self, id):
        return id

    def delete(self, id):
        return id

    def show(self, id):
        return id

    def edit(self, id):
        return id
    

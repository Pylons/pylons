from projectname.tests import *

class TestMakoController(TestController):
    def test_mako(self):
        response = self.app.get(url(controller='sample', action='testmako'))
        assert 'Hello, 5+5 is 10' in response

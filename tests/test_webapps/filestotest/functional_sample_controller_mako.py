from projectname.tests import *

class TestCheetahController(TestController):
    def test_mako(self):
        response = self.app.get(url_for(controller='/sample', action='testmako'))
        assert 'Hello, 5+5 is 10' in response

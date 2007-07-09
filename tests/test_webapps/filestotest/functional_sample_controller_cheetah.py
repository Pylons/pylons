from projectname.tests import *

class TestCheetahController(TestController):
    def test_cheetah(self):
        response = self.app.get(url_for(controller='/sample', action='testcheetah'))
        assert 'Hello from Cheetah' in response
        assert 'This is in c var' in response
        assert '--Empty var: --' in response

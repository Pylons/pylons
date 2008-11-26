from projectname.tests import *

class TestJinja2Controller(TestController):
    def test_jinja2(self):
        response = self.app.get(url(controller='sample', action='testjinja2'))
        assert 'Hello from Jinja2' in response
        assert 'This is in c var' in response

from projectname.tests import *

class TestSample2Controller(TestController):
    def test_session(self):
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session.has_key('counter')
        assert response.session['counter'] == 0
        
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session['counter'] == 1
        assert 'session incrementer' in response
        
    def test_default(self):
        response = self.app.get(url(controller='sample', action='test_template_caching'))
        assert 'Hi everyone!' in response
    
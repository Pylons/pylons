from projectname.tests import *

class TestSample2Controller(TestController):
    def test_session(self):
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session.has_key('counter')
        assert response.session['counter'] == 0
        
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session['counter'] == 1
        assert 'session incrementer' in response
    
    def test_kid_default(self):
        response = self.app.get(url(controller='sample', action='testdefault'))
        assert 'Hello from Kid' in response
        assert 'This is in c var' in response
        assert '--Empty var: --' in response

from projectname.tests import *

class TestSample2Controller(TestController):
    def test_session(self):
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session.has_key('counter')
        assert response.session['counter'] == 0
        
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session['counter'] == 1
        assert 'session incrementer' in response
    
    def test_genshi_default(self):
        self._test_genshi_default('testdefault')
    
    def _test_genshi_default(self, action):
        response = self.app.get(url(controller='sample', action=action))
        assert 'Hello from Genshi' in response
        assert 'This is in c var' in response

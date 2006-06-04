from projectname.tests import *

class TestTest2Controller(TestController):
    def test_session(self):
        response = self.app.get(url_for(controller='/test1', action='session_increment'))
        assert response.session.has_key('counter')
        assert response.session['counter'] == 0
        
        response = self.app.get(url_for(controller='/test1', action='session_increment'))
        assert response.session['counter'] == 1
        assert 'session incrementer' in response
    
    def test_kid_default(self):
        response = self.app.get(url_for(controller='/test1', action='testdefault'))
        assert 'Hello from Kid' in response
    
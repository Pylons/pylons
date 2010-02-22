from projectname.tests import *

class TestSampleController(TestController):
    def test_root_index(self):
        response = self.app.get('/')
        assert 'Welcome' in response
        # Test response...
    
    def test_index(self):
        response = self.app.get(url(controller='sample', action='index'))
        assert 'basic index page' in response
    
    def test_session(self):
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session.has_key('counter')
        assert response.session['counter'] == 0
        
        response = self.app.get(url(controller='sample', action='session_increment'))
        assert response.session['counter'] == 1
        assert 'session incrementer' in response
    
    def test_global(self):
        response = self.app.get(url(controller='sample', action='globalup'))
        assert 'Hello' in response
    
    def test_global_persistence(self):
        response = self.app.get(url(controller='sample', action='global_store'))
        assert '0' in response
        
        response = self.app.get(url(controller='sample', action='global_store', id=2))
        assert '2' in response
        
        response = self.app.get(url(controller='sample', action='global_store'))
        assert '2' in response
        
        response = self.app.get(url(controller='sample', action='global_store', id=3))
        assert '5' in response
        
        response = self.app.get(url(controller='sample', action='global_store'))
        assert '5' in response
    
    def test_helper_urlfor(self):
        response = self.app.get(url(controller='sample', action='myself'))
        assert 'sample/myself' in response
    
    def test_params(self):
        response = self.app.get(url(controller='sample', action='myparams', extra='something', data=4))
        assert 'extra' in response
        assert 'something' in response
        assert 'data' in response

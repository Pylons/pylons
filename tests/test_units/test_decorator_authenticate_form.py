# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os

from beaker.middleware import SessionMiddleware
from paste.fixture import TestApp
from paste.registry import RegistryManager
from routes import request_config

from __init__ import data_dir, TestWSGIController

session_dir = os.path.join(data_dir, 'session')

try:
    import shutil
    shutil.rmtree(session_dir)
except:
    pass


# Eat the logging handler messages
my_logger = logging.getLogger()
my_logger.setLevel(logging.INFO)
# Add the log message handler to the logger
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
my_logger.addHandler(NullHandler())


def make_protected():
    from pylons.controllers import WSGIController
    from pylons.decorators.secure import authenticate_form
    from webhelpers.pylonslib import secure_form
    from pylons import request
    
    class ProtectedController(WSGIController):
        def form(self):
            request_config().environ = request.environ
            return secure_form.authentication_token()

        @authenticate_form
        def protected(self):
            request_config().environ = request.environ
            return 'Authenticated'
    return ProtectedController


class TestAuthenticateFormDecorator(TestWSGIController):
    def setUp(self):
        from pylons.testutil import ControllerWrap, SetupCacheGlobal
        ProtectedController = make_protected()
        TestWSGIController.setUp(self)
        app = ControllerWrap(ProtectedController)
        app = SetupCacheGlobal(app, self.environ, setup_session=True)
        app = SessionMiddleware(app, {}, data_dir=session_dir)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_unauthenticated(self):
        from pylons.decorators.secure import csrf_detected_message
        
        self.environ['pylons.routes_dict']['action'] = 'protected'
        response = self.app.post('/protected', extra_environ=self.environ,
                                 expect_errors=True)
        assert response.status == 403
        assert csrf_detected_message in response

    def test_authenticated(self):
        from webhelpers.pylonslib import secure_form
        
        self.environ['pylons.routes_dict']['action'] = 'form'
        response = self.app.get('/form', extra_environ=self.environ)
        token = response.body

        self.environ['pylons.routes_dict']['action'] = 'protected'
        response = self.app.post('/protected',
                                 params={secure_form.token_key: token},
                                 extra_environ=self.environ,
                                 expect_errors=True)
        assert 'Authenticated' in response

        self.environ['pylons.routes_dict']['action'] = 'protected'
        response = self.app.put('/protected',
                                params={secure_form.token_key: token},
                                extra_environ=self.environ,
                                expect_errors=True)
        assert 'Authenticated' in response

        # GET with token_key in query string
        response = self.app.get('/protected',
                                 params={secure_form.token_key: token},
                                 extra_environ=self.environ,
                                 expect_errors=True)
        assert 'Authenticated' in response

        # POST with token_key in query string
        response = self.app.post('/protected?' + secure_form.token_key + '=' + token,
                                 extra_environ=self.environ,
                                 expect_errors=True)
        assert 'Authenticated' in response

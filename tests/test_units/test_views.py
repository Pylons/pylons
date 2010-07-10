import unittest

class LegacyViewTests(unittest.TestCase):
    def _makeOne(self, app):
        from pylons.views import LegacyView
        return LegacyView(app)

    def test_it(self):
        request = DummyRequest()
        view = self._makeOne(dummyapp)
        response = view(request)
        self.assertEqual(response, dummyapp)

def dummyapp(environ, start_response):
    """ """

class DummyRequest:
    def get_response(self, application):
        return application

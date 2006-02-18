from pylons import Controller, m, h, c, session, request
import translate_demo.model as model
g = request.environ['pylons.g']

class BaseController(Controller):
    def __call__(self, action, **params):
        # Insert any code to be run per request here
        Controller.__call__(self, action, **params)
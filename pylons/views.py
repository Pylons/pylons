class LegacyView(object):
    def __init__(self, app):
        self.app = app # app is the legacy Pylons app

    def __call__(self, request):
        return request.get_response(self.app)
    

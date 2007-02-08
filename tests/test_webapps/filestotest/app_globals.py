class Globals(object):

    def __init__(self, global_conf, app_conf, **extra):
        self.message = 'Hello'
        self.counter = 0
        
    def __del__(self):
        """
        Put any cleanup code to be run when the application finally exits 
        here.
        """
        pass

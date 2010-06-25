"""Events

Pylons events are triggered in various stages during a Pylons application's execution
and setup. They can be registered using the :func:`~pylons.events.subscriber`
decorator or directly with the config object::
    
    config.add_subscriber(my_subscriber, NewRequest)

"""
import venusian

def subscriber(*events):
    """Register a function for an event, or multiple events
    
    Example::
        
        from pylons.events import subscriber, NewRequest
        
        @subscriber(NewRequest)
        def check_user(event):
            req = event.request
            req.user_name = environ.get('REMOTE_USER')
            return
    
    Event subscribers are not expected to return values, and any
    values returned will be ignored.
    
    """
    def func_wrapper(wrapped):
        def callback(scanner, name, ob):
            for event in events:
                scanner.config.add_subscriber(wrapped, event)
        venusian.attach(wrapped, callback, category='pylons')
        return wrapped
    return func_wrapper


class NewRequest(object):
    """ An instance of this class is emitted as an event whenever
    Pylons begins to process a new request.  The instance has an
    attribute, ``request``, which is the request object."""
    def __init__(self, request):
        self.request = request


class NewResponse(object):
    """ An instance of this class is emitted when a response is
    recieved by Pylons, right before its sent out to the client. The
    instance has an attribute, ``response``, which is the response
    object."""
    def __init__(self, response):
        self.response = response

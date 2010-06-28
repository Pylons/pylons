"""View functions and classes"""
import logging

import pkg_resources
from webob.exc import HTTPException, HTTPNotFound

log = logging.getLogger(__name__)


class DelayedView(object):
    def __init__(self, route_name):
        self.route_name = route_name
        self.views = []
    
    def __call__(self, request):
        try:
            return self.view(request)
        except AttributeError:
            raise Exception('No view registered for route: %s' % self.route_name)
    
    def finalize(self):
        pass
        #self.view = multi_view(self.views)


def multi_view(views):
    """Creates a view that evaluates predicates to call the view that
    matches the most
    
    Initialized with a list of tuples in the format::
        
        (view_responder, predicates)
    
    """
    

def lookup_view(view, package_name=None):
    """Load a view based on a resource specification"""
    return pkg_resources.EntryPoint.parse('x=%s' % view).load(False)


def map_view(config, args, kwargs):
    """Given a responder name, handle looking it up and returning
    a callable responder"""
    view = kwargs.pop('view', None)
    
    # If no view was listed, this should have a view added later unless
    # a responder is being added directly
    if not view and 'responder' not in kwargs:
        # The first arg is assumed to be a route name
        if len(args) < 2:
            raise Exception("When adding a route with no view, a route "
                            " name must be specified. Route: %s", args[0])
        route_name = args[0]
        dv = DelayedView(route_name)
        kwargs['responder'] = config._delayed_views[route_name] = dv
        return args, kwargs
    elif 'responder' in kwargs:
        # We have a responder directly, retain it
        return args, kwargs
    
    # If its a string, determine if its a legacy controller name
    # or a resource specification
    if isinstance(view, basestring):
        view_result = lookup_view(view)
    else:
        view_result = view
    
    # If it has an action, assume we can pick the action off it
    if hasattr(view_result, '__bases__'):
        kwargs['responder'] = class_responder(view_result, kwargs.get('action'))
    else:
        kwargs['responder'] = func_inst_responder(view_result, kwargs.get('action'))
    return args, kwargs


def class_responder(view, action=None):
    """view_responder wraps a single class based view with a responder
    interface
    
    If the action is a method, the class will be instantiated with a
    request object, and the method will then be called with no
    arguments.
    
    If there is no action specified, then the class will be called
    after its instantiated (a __call__ should be implemented).
    
    The __init__ method may raise an HTTPException should it wish to
    terminate calling, at which point it will be returned to the client.
    
    """
    if action:
        if not hasattr(view, action):
            raise Exception("Unable to locate method %s on %r" % (action, view))
        action = getattr(view, action)
    
    def view_wrapper(request):
        """The view that is dispatched to by Pylons
        
        This wrapper implements the responder paradigm.
        
        """
        # Instantiate the controller with the request
        view_obj = view(request)
        if action:
            response = action(view_obj)
        else:
            response = view_obj()
        return response
    return view_wrapper


def func_inst_responder(view, action=None):
    """func_inst_responder wraps a function or callable
    
    If an action is supplied, it must be an attribute on the view that
    is callable with a request, and returns a response.
    
    """
    if action:
        if not hasattr(view, action):
            raise Exception("Unable to locate method %s on %r" % (action, view))
        view_obj = getattr(view, action)
    else:
        view_obj = view
    
    def view_wrapper(request):
        """The view that is dispatched to by Pylons
        
        This wrapper implements the responder paradigm.
        
        """
        return view_obj(request)
    return view_wrapper

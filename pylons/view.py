"""View functions and classes"""
import logging

import pkg_resources
from webob.exc import HTTPException, HTTPNotFound

log = logging.getLogger(__name__)


def lookup_view(view, package_name=None):
    """Load a view based on a resource specification"""
    return pkg_resources.EntryPoint.parse('x=%s' % view).load(False)


def map_view(config, args, kwargs):
    """Given a responder name, handle looking it up and returning
    a callable responder"""
    view = kwargs.pop('view', None)
    
    # If no view was listed, this should have a view added later unless
    # a responder is being added directly
    # if not view and 'responder' not in kwargs:
    #     # The first arg is assumed to be a route name
    #     if len(args) < 2:
    #         raise Exception("When adding a route with no view, a route "
    #                         " name must be specified. Route: %s", args[0])
    #     route_name = args[0]
    #     dv = DelayedView(route_name)
    #     kwargs['responder'] = config._delayed_views[route_name] = dv
    #     return args, kwargs
    # elif 'responder' in kwargs:
    #     # We have a responder directly, retain it
    #     return args, kwargs
    
    # If its a string, determine if its a legacy controller name
    # or a resource specification
    if isinstance(view, basestring):
        view_result = lookup_view(view)
    else:
        view_result = view
    
    if hasattr(view_result, '__bases__'):
        # Class based view, if we have an action we register just the route_responder
        # for that action, otherwise its a multi-view, so we register a
        # multi_route_responder
        if 'action' in kwargs:
            kwargs['responder'] = view_responder(view_result, kwargs['action'])
        else:
            kwargs['responder'] = view_responder(view_result)
    else:
        # It's a plain view callable
        if not callable(view_result):
            raise Exception("Can't map %s to a valid view callable, got"
                            " %r instead.", view, view_result)
        kwargs['responder'] = view_result
    return args, kwargs


def view_responder(view, action=None):
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
        log_debug = request.environ['pylons.log_debug']
        
        # Instantiate the controller with the request, if it raises an
        # HTTPException, return it
        try:
            view_obj = view(request)
        except HTTPException, httpe:
            return httpe
                
        try:
            if action:
                response = action(view_obj)
            else:
                response = view_obj()
        except HTTPException, httpe:
            response = httpe
        except TypeError:
            # Raised when attempting to call a non-callable
            if log_debug:
                log.debug("Can't call non-callable view %r", action or view_obj)
            response = HTTPNotFound()
        return response
    return view_wrapper

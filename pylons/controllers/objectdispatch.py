from decorated import DecoratedController
from util import to_kw, from_kw
from formencode.variabledecode import variable_decode
from paste import httpexceptions

import pylons
import urlparse
import formencode


class ObjectDispatchController(DecoratedController):
    """
    To use Object Dispatch, create a route for *URL and point it to the 
    route method of an ObjectDispatchController.  The controller will 
    then thake the remainder of the URL, and do Object dispatch on it. 
    
    The oject dispatch controller looks through your class to find matching methods, 
    walking down the object hierarchy untill a match is found.  A classes Index 
    matches and the default method is called if no matching method is called.
    
    Like the underlying DecoratedController, controller methods can only be
    called if you explicitly expose them to the web using an @expose decorator.  

    In addition to CherryPy style Object dispatch, this controller also 
    implements a Quxote inspired ookup method which allows you to create new objects
    to dispatch against at any time. 

    *lookup* and *default* controller methods are called in identical situations: 
    when "normal" object traversal is not able to find an exposed method, 
    the controller begins popping the stack of "not found" handlers.  
    
    If the handler is a "default" method, it is called with the rest of the 
    path as positional parameters passed into the default method.   

    The not found handler stack can also contain "lookup" methods, which
    are different, as they are not actual controllers. 

    A lookup method takes as its argument the remaining path elements and
    returns an object (representing the next step in the traversal) and a
    (possibly modified) list of remaining path elements.  So a blog might
    have controllers that look something like this:

    class BlogController(Controller):
       @expose()
       def lookup(self, year, month, day, id, *remainder):
          dt = date(int(year), int(month), int(day))
          return BlogEntryController(dt, int(id)), remainder

    class BlogEntryController(Controller):
       def __init__(self, dt, id):
           self.entry = model.BlogEntry.get_by(date=dt, id=id)
    
       @expose(...)
           def index(self):
           ...
     
       @expose(...)
           def edit(self):
           ...
           
       @expose()
       def update(self):
            ....

    So a URL request to .../2007/6/28/0/edit would map to
    BlogEntryController(date(2007,6,28), 0).edit .  In other situations, 
    you might have a several-layers-deep "lookup" chain, e.g. for 
    editing hierarchical data (/client/1/project/2/task/3/edit).  

    The benefit over "default" handlers is that you _return_ a controller 
    and continue traversing rather than _being_ a controller and 
    stopping traversal altogether.  Plus, it makes semi-RESTful URLs easy.
    """
    
    def _initialize_validation_context(self):
        pylons.c.form_errors = {}
        pylons.c.form_values = {}
    
    def _get_routing_info(self, url=None):
        """
        Returns a tuple (controller, remainder, params) 
        
        :Parameters:
          url
            url as string
        """
        if url is None:
            url_path = pylons.request.path_info.split('/')[1:]
        else:
            url_path = url.split('/')

        controller, remainder = object_dispatch(self, url_path)
        #XXX Place controller url at context temporarily... we should be
        #    really using SCRIPT_NAME for this.
        if remainder:
            pylons.c.controller_url = '/'.join(url_path[:-len(remainder)])
        else:
            pylons.c.controller_url = url
        if remainder and remainder[-1] == '': remainder.pop()
        return controller, remainder, pylons.request.params    
    
    def _perform_call(self, func, args):
        self._initialize_validation_context()
        controller, remainder, params = self._get_routing_info(args['url'])
        return DecoratedController._perform_call(self, controller, params, remainder=remainder)
    
    def route(self, url='/', start_response=None, **kw):
        pass


def object_dispatch(obj, url_path):
    remainder = url_path
    notfound_handlers = []
    while True:
        try:
            obj, remainder = find_object(obj, remainder, notfound_handlers)
            return obj, remainder
        except httpexceptions.HTTPNotFound, err:
            if not notfound_handlers: raise
            name, obj, remainder = notfound_handlers.pop()
            if name == 'default': return obj, remainder
            else:
                obj, remainder = obj(*remainder)
                continue


def find_object(obj, remainder, notfound_handlers):
    while True:
        if obj is None: raise httpexceptions.HTTPNotFound()
        if iscontroller(obj): return obj, remainder

        if not remainder or remainder == ['']:
            index = getattr(obj, 'index', None)
            if iscontroller(index): return index, remainder

        default = getattr(obj, 'default', None)
        if iscontroller(default):
            notfound_handlers.append(('default', default, remainder))

        lookup = getattr(obj, 'lookup', None)
        if iscontroller(lookup):
            notfound_handlers.append(('lookup', lookup, remainder))

        if not remainder: raise httpexceptions.HTTPNotFound()
        obj = getattr(obj, remainder[0], None)
        remainder = remainder[1:]
    
            
def iscontroller(obj):
    if not hasattr(obj, '__call__'): return False
    if not hasattr(obj, 'decoration'): return False
    return obj.decoration.exposed
"""Standard Controllers intended for sub-classing by web developers"""
import sys
import types
import inspect
import types
import warnings
import xmlrpclib

from paste.httpexceptions import HTTPException
from paste.deploy.converters import asbool

import pylons
from pylons.helpers import abort

XMLRPC_MAPPING = {str:'string', list:'array', int:'int', bool:'boolean',
                  float:'double', dict:'struct', 
                  xmlrpclib.DateTime:'dateTime.iso8601',
                  xmlrpclib.Binary:'base64'}

def xmlrpc_sig(args):
    """Returns a list of the function signature in string format based on a 
    tuple provided by xmlrpclib."""
    signature = []
    for param in args:
        for type, xml_name in XMLRPC_MAPPING.iteritems():
            if isinstance(param, type):
                signature.append(xml_name)
                break
    return signature

def xmlrpc_fault(code, message):
    """Convienence method to return a Pylons response XMLRPC Fault"""
    fault = xmlrpclib.Fault(code, message)
    return pylons.Response(xmlrpclib.dumps(fault, methodresponse=True))

def trim(docstring):
    """Yanked from PEP 237, strips the whitespace from Python doc strings"""
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

class Controller(object):
    """Standard Pylons Controller for Web Requests
    
    The Pylons Controller handles incoming web requests that are dispatched
    from the custom Myghty Routes resolver. These requests result in a new
    instance of the Controller being created, which is then called with the
    dict options from the Routes match.
    
    By default, the Controller will search and attempt to call a ``__before__``
    method before calling the action, and will try to call a ``__after__``
    method after the action was called. These two methods can act as filters
    controlling access to the action, setup variables/objects for use with a
    set of actions, etc.
    
    Each action to be called is inspected with ``_inspect_call`` so that it is
    only passed the arguments in the Routes match dict that it asks for. The only
    exception to the dict is that the Myghty ``ARGS`` variable is included.
    
    In the event that an action is not found to handle the request, the Controller
    will raise an "Action Not Found" error if in debug mode, otherwise a ``404 Not Found``
    error will be returned.
    """
    __pudge_all__ = ['_inspect_call', '__call__', '_attach_locals']
    
    def _attach_locals(self):
        """Attach Pylons special objects to the controller
        
        When debugging, the Pylons special objects are unavailable because they
        are thread locals. This function pulls the actual object and attaches it
        to the controller so that it can be examined for debugging purposes.

        Deprecated (Nov 30 2006); Pylons special objects are now available
        within the interactive debugger.
        """
        warnings.warn('_attach_locals is deprecated: Pylons special objects '
                      'are now available within the interactive debugger',
                      DeprecationWarning, 2)
        self.c = pylons.c._current_obj()
        self.g = pylons.g._current_obj()
        self.cache = pylons.cache._current_obj()
        self.session = pylons.session._current_obj()
        self.request = pylons.request._current_obj()
        self.buffet = pylons.buffet._current_obj()

    def _inspect_call(self, func, **kargs):
        """Calls a function with as many arguments from args and kargs as
        possible
        
        Given a function, inspect_call will inspect the function args and call
        it with no further keyword args than it asked for.
        
        If the function has been decorated, it is assumed that the decorator
        preserved the function signature.
        """
        argspec = inspect.getargspec(func)
        kargs = self._get_method_args()
        
        # Hide the traceback for everything above this controller
        __traceback_hide__ = 'before_and_this'
        
        c = pylons.c._current_obj()
        if argspec[2]:
            for k, val in kargs.iteritems():
                setattr(c, k, val)
            result = func(**kargs)
        else:
            args = []
            argnames = argspec[0][1:]
            for name in argnames:
                if name in kargs:
                    setattr(c, name, kargs[name])
                    args.append(kargs[name])
            result = func(*args)
        if isinstance(result, types.GeneratorType):
            return pylons.Response(result)
        else:
            return result

    def _get_method_args(self):
        """Retrieve the method arguments to use with inspect call
        
        By default, this uses Routes to retrieve the arguments, override
        this method to customize the arguments your controller actions are
        called with."""
        req = pylons.request._current_obj()
        kargs = req.environ['pylons.routes_dict'].copy()
        kargs.update(dict(environ=req.environ, 
                          start_response=self.start_response))
        return kargs
    
    def _dispatch_call(self):
        """Handles dispatching the request to the function using Routes"""
        req = pylons.request._current_obj()
        action = req.environ['pylons.routes_dict'].get('action')
        action_method = action.replace('-', '_')
        func = getattr(self, action_method, None)
        if isinstance(func, types.MethodType):
            response = self._inspect_call(func)
        else:
            if asbool(req.environ['paste.config']['global_conf'].get('debug')):
                raise NotImplementedError(
                    'Action %s is not implemented' % action)
            else:
                response = pylons.Response(code=404)
        return response
    
    def __call__(self, *args, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        """
        req = pylons.request._current_obj()
        
        # Keep private methods private
        if req.environ['pylons.routes_dict'].get('action', '').startswith('_'):
            return pylons.Response(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)

        if not hasattr(self, '__after__'):
            response = self._dispatch_call()
        else:
            try:
                response = self._dispatch_call()
            except HTTPException:
                self._inspect_call(self.__after__)
                raise
            self._inspect_call(self.__after__)
        return response

class WSGIController(Controller):
    """WSGI Controller that follows WSGI spec for calling and return values
    
    This function works identically to the normal Controller, however it is called
    with the WSGI interface, and behaves as a WSGI application calling start_response
    and returning an iterable as content.
    """
    def __call__(self, environ, start_response):
        self.start_response = start_response
        
        # Keep private methods private
        if environ['pylons.routes_dict'].get('action', '').startswith('_'):
            return pylons.Response(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__)

        if not hasattr(self, '__after__'):
            response = self._dispatch_call()
        else:
            try:
                response = self._dispatch_call()
            except HTTPException:
                self._inspect_call(self.__after__)
                raise
            self._inspect_call(self.__after__)
        
        if hasattr(response, 'wsgi_response'):
            # Copy the response object into the testing vars if we're testing
            if 'paste.testing_variables' in environ:
                environ['paste.testing_variables']['response'] = response
            return response(environ, start_response)
        
        return response

class XMLRPCController(WSGIController):
    """XML-RPC Controller"""

    max_body_length = 4194304

    def _get_method_args(self):
        return self.rpc_kargs

    def __call__(self, environ, start_response):
        # Pull out the length, return an error if there is no valid
        # length or if the length is larger than the max_body_length.
        length = environ.get('CONTENT_LENGTH')
        if length:
            length = int(length)
        else:
            # No valid Content-Length header found
            abort(411)
        if length > self.max_body_length or length == 0:
            abort(413, "XML body too large")

        body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
        rpc_args, orig_method = xmlrpclib.loads(body)
        
        method = self._find_method_name(orig_method)
        if not hasattr(self, method):
            return xmlrpc_fault(0, "No method by that name")

        func = getattr(self, method)

        # Signature checking for params
        if hasattr(func, 'signature'):
            valid_args = False
            params = xmlrpc_sig(rpc_args)
            for sig in func.signature:
                # Next sig if we don't have the same amount of args
                if len(sig)-1 != len(rpc_args):
                    continue

                # If the params match, we're valid
                if params == sig[1:]:
                    valid_args = True
                    break

            if not valid_args:
                return xmlrpc_fault(0, "Incorrect argument signature. %s recieved does "
                                    "not match %s signature for method %s" % \
                                    (params, func.signature, orig_method))

        # Change the arg list into a keyword dict based off the arg
        # names in the functions definition
        arglist = inspect.getargspec(func)[0][1:]
        kargs = dict(zip(arglist, rpc_args))
        kargs['action'], kargs['environ'] = method, environ
        kargs['start_response'] = start_response
        self.rpc_kargs = kargs
        self._func = func

        # Now that we know the method is valid, and the args are valid,
        # we can dispatch control to the default WSGIController
        return WSGIController.__call__(self, environ, start_response)

    def _dispatch_call(self):
        """Dispatch the call to the function chosen by __call__"""
        raw_response = self._inspect_call(self._func)
        if not isinstance(raw_response, xmlrpclib.Fault):
            raw_response = (raw_response,)

        response = xmlrpclib.dumps(raw_response, methodresponse=True)
        return pylons.Response(response)

    def _find_method_name(self, name):
        return name.replace('.', '_')

    def _publish_method_name(self, name):
        return name.replace('_', '.')

    def system_listMethods(self):
        """Returns a list of XML-RPC methods for this XML-RPC resource"""
        methods = []
        for method in dir(self):
            meth = getattr(self, method)

            # Only methods have this attribute
            if not method.startswith('_') and hasattr(meth, 'im_self'):
                methods.append(self._publish_method_name(method))
        return methods
    system_listMethods.signature = [ ['array'] ]

    def system_methodSignature(self, name):
        """Returns an array of array's for the valid signatures for a method.

        The first value of each array is the return value of the method. The
        result is an array to indicate multiple signatures a method may be
        capable of.
        """
        if hasattr(self, name):
            method = getattr(self, name)
            if hasattr(method, 'signature'):
                return getattr(method, 'signature')
            else:
                return ''
        else:
            return xmlrpclib.Fault(0, 'No such method name')
    system_methodSignature.signature = [ ['array', 'string'],
                                         ['string', 'string'] ]

    def system_methodHelp(self, name):
        """Returns the documentation for a method"""
        if hasattr(self, name):
            method = getattr(self, name)
            help = getattr(method, 'help', None) or method.__doc__
            help = trim(help)
            sig = getattr(method, 'signature', None)
            if sig:
                help += "\n\nMethod signature: %s" % sig
            return help
        return xmlrpclib.Fault(0, "No such method name")
    system_methodHelp.signature = [ ['string', 'string'] ]

    
__all__ = ['Controller', 'WSGIController', 'XMLRPCController']

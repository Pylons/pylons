"""Standard Controllers intended for sub-classing by web developers"""
import inspect
import logging
import sys
import types
import warnings
import xmlrpclib

from paste.httpexceptions import HTTPException
from paste.response import replace_header, HeaderDict
from paste.wsgiwrappers import WSGIResponse

import pylons
from pylons.helpers import abort

__all__ = ['Controller', 'WSGIController', 'XMLRPCController']


XMLRPC_MAPPING = ((basestring, 'string'), (list, 'array'), (bool, 'boolean'),
                  (int, 'int'), (float, 'double'), (dict, 'struct'), 
                  (xmlrpclib.DateTime, 'dateTime.iso8601'),
                  (xmlrpclib.Binary, 'base64'))


log = logging.getLogger(__name__)


def xmlrpc_sig(args):
    """Returns a list of the function signature in string format based on a 
    tuple provided by xmlrpclib."""
    signature = []
    for param in args:
        for type, xml_name in XMLRPC_MAPPING:
            if isinstance(param, type):
                signature.append(xml_name)
                break
    return signature


def xmlrpc_fault(code, message):
    """Convienence method to return a Pylons response XMLRPC Fault"""
    fault = xmlrpclib.Fault(code, message)
    return WSGIResponse(xmlrpclib.dumps(fault, methodresponse=True))


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


class WSGIController(object):
    """WSGI Controller that follows WSGI spec for calling and return values
    
    The Pylons WSGI Controller handles incoming web requests that are 
    dispatched from the PylonsBaseWSGIApp. These requests result in a new 
    instance of the WSGIController being created, which is then called with the
    dict options from the Routes match. The standard WSGI response is then
    returned with start_response called as per the WSGI spec.
    
    By default, the WSGIController will search and attempt to call a 
    ``__before__`` method before calling the action, and will try to call a
    ``__after__`` method after the action was called. These two methods can act
    as filters controlling access to the action, setup variables/objects for 
    use with a set of actions, etc.
    
    Each action to be called is inspected with ``_inspect_call`` so that it is
    only passed the arguments in the Routes match dict that it asks for. The
    arguments passed into the action can be customized by overriding the 
    ``_get_method_args`` function which is expected to return a dict.
    
    In the event that an action is not found to handle the request, the
    Controller will raise an "Action Not Found" error if in debug mode,
    otherwise a ``404 Not Found`` error will be returned.
    """
    
    __pudge_all__ = ['_inspect_call', '__call__', '_get_method_args', 
                     '_dispatch_call']
    
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
        args = None
        if argspec[2]:
            for k, val in kargs.iteritems():
                setattr(c, k, val)
            args = kargs
        else:
            args = {}
            argnames = argspec[0][1:]
            for name in argnames:
                if name in kargs:
                    setattr(c, name, kargs[name])
                    args[name] = kargs[name]
        log.debug("Calling '%s' method with keyword arguments: **%s",
                  func.__name__, args)
        try:
            result = func(**args)
            log.debug("'%s' method returned a response", func.__name__)
        except HTTPException, httpe:
            log.debug("'%s' method resulted in HTTP Exception: %s", 
                      func.__name__, httpe)
            result = httpe.response(pylons.request.environ)
            result._exception = True
        return result
    
    def _get_method_args(self):
        """Retrieve the method arguments to use with inspect call
        
        By default, this uses Routes to retrieve the arguments, override
        this method to customize the arguments your controller actions are
        called with.
        """
        req = pylons.request._current_obj()
        kargs = req.environ['pylons.routes_dict'].copy()
        kargs['environ'] = req.environ
        if hasattr(self, 'start_response'):
            kargs['start_response'] = self.start_response
        return kargs
    
    def _dispatch_call(self):
        """Handles dispatching the request to the function using Routes"""
        req = pylons.request._current_obj()
        action = req.environ['pylons.routes_dict'].get('action')
        action_method = action.replace('-', '_')
        log.debug("Looking for '%s' method to handle the request", action_method)
        func = getattr(self, action_method, None)        
        if isinstance(func, types.MethodType):
            # Store function used to handle request
            req.environ['pylons.action_method'] = func
            
            response = self._inspect_call(func)
        else:
            log.debug("Couldn't find '%s' method to handle response", action)
            if pylons.config['debug']:
                raise NotImplementedError('Action %s is not implemented' %
                                          action)
            else:
                response = WSGIResponse(code=404)
        return response
    
    def __call__(self, environ, start_response):
        start_response_called = []
        def repl_start_response(status, headers, exc_info=None):
            response = pylons.response._current_obj()
            start_response_called.append(None)
            
            # Copy the headers from the global response in if its a 2XX or
            # 3XX status code
            # XXX: TODO: This should really be done with a more efficient 
            #            header merging function at some point.
            if status.startswith('2'):
                response.headers.update(HeaderDict.fromlist(headers))
                headers = response.headers.headeritems()
                log.debug("Merging headers into start_response call, "
                          "status: %s", status)
            if status.startswith('3') or status.startswith('2'):
                for c in pylons.response.cookies.values():
                    headers.add('Set-Cookie', c.output(header=''))
                log.debug("Merging cookies into start_response call, "
                          "status: %s", status)
            return start_response(status, headers, exc_info)
        self.start_response = repl_start_response
        
        # Keep private methods private
        if environ['pylons.routes_dict'].get('action', '').startswith('_'):
            log.debug("Action starts with _, private action not allowed. "
                      "Returning a 404 response")
            return WSGIResponse(code=404)(environ, start_response)
        
        if hasattr(self, '__before__'):
            log.debug("Calling __before__ action")
            response = self._inspect_call(self.__before__)
            if hasattr(response, '_exception'):
                return response(environ, start_response)
        
        response = self._dispatch_call()
        if not start_response_called:
            # If its not a WSGI response, and we have content, it needs to
            # be wrapped in the response object
            if hasattr(response, 'wsgi_response'):
                # It's either a legacy WSGIResponse object, or an exception
                # that got tossed. Strip headers if its anything other than a
                # 2XX status code, and strip cookies if its anything other than
                # a 2XX or 3XX status code.
                if response.status_code < 300:
                    log.debug("Merging global headers into returned response"
                              " object")
                    response.headers.update(pylons.response.headers)
                if response.status_code < 400:
                    log.debug("Merging global cookies into returned response"
                              " object")
                    for c in pylons.response.cookies.values():
                        response.headers.add('Set-Cookie', c.output(header=''))
                registry = environ['paste.registry']
                registry.replace(pylons.response, response)
                log.debug("Replaced global response object with returned one")
            elif isinstance(response, types.GeneratorType):
                pylons.response.content = response
                log.debug("Set response content to returned generator")
            elif isinstance(response, basestring):
                pylons.response.write(response)
                log.debug("Set response content to returned string data")
            response = pylons.response._current_obj()
        
        if hasattr(self, '__after__'):
            log.debug("Calling __after__ action")
            after = self._inspect_call(self.__after__)
            if hasattr(after, '_exception'):
                return after(environ, start_response)
        
        if hasattr(response, 'wsgi_response'):
            # Copy the response object into the testing vars if we're testing
            if 'paste.testing_variables' in environ:
                environ['paste.testing_variables']['response'] = response
            log.debug("Calling response object to return WSGI data")
            return response(environ, start_response)
        
        log.debug("Response assumed to be WSGI content, returning un-touched")
        return response


class Controller(WSGIController):
    """Deprecated Pylons Controller for Web Requests
    
    All Pylons projects should use the WSGIController.
    """
    def __init__(self, *args, **kwargs):
        warnings.warn("Controller class is deprecated, switch to using the"
                      "WSGIController class", DeprecationWarning, 2)
        WSGIController.__init__(self, *args, **kwargs)
    
    def __call__(self, *args, **kargs):
        """Makes our controller a callable to handle requests
        
        This is called when dispatched to as the Controller class docs explain
        more fully.
        """
        req = pylons.request._current_obj()
        
        # Keep private methods private
        if req.environ['pylons.routes_dict'].get('action', '').startswith('_'):
            return WSGIResponse(code=404)
        
        if hasattr(self, '__before__'):
            self._inspect_call(self.__before__, **kargs)
        response = self._dispatch_call()
        
        # If its not a WSGI response, and we have content, it needs to
        # be wrapped in the response object
        if hasattr(response, 'wsgi_response'):
            # It's either a legacy WSGIResponse object, or an exception
            # that got tossed. Strip headers if its anything other than a
            # 2XX status code, and strip cookies if its anything other than
            # a 2XX or 3XX status code.
            if response.status_code < 300:
                response.headers.update(pylons.response.headers)
            if response.status_code < 400:
                for c in pylons.response.cookies.values():
                    response.headers.add('Set-Cookie', c.output(header=''))
            registry = req.environ['paste.registry']
            registry.replace(pylons.response, response)
        elif isinstance(response, types.GeneratorType):
            pylons.response.content = response
        elif isinstance(response, basestring):
            pylons.response.write(response)
        response = pylons.response._current_obj()
        
        if hasattr(self, '__after__'):
            self._inspect_call(self.__after__)
        
        return response


class XMLRPCController(WSGIController):
    """XML-RPC Controller that speaks WSGI
    
    This controller handles XML-RPC responses and complies with the 
    `XML-RPC Specification <http://www.xmlrpc.com/spec>`_ as well as the
    `XML-RPC Introspection <http://scripts.incutio.com/xmlrpc/introspection.html>`_
    specification.
    
    By default, methods with names containing a dot are translated to use an
    underscore. For example, the `system.methodHelp` is handled by the method 
    `system_methodHelp`.
    
    Methods in the XML-RPC controller will be called with the method given in 
    the XMLRPC body. Methods may be annotated with a signature attribute to 
    declare the valid arguments and return types.
    
    For example::
        
        class MyXML(XMLRPCController):
            def userstatus(self):
                return 'basic string'
            userstatus.signature = [ ['string'] ]
            
            def userinfo(self, username, age=None):
                user = LookUpUser(username)
                response = {'username':user.name}
                if age and age > 10:
                    response['age'] = age
                return response
            userinfo.signature = [ ['struct', 'string'], ['struct', 'string', 'int'] ]
    
    Since XML-RPC methods can take different sets of data, each set of valid
    arguments is its own list. The first value in the list is the type of the
    return argument. The rest of the arguments are the types of the data that
    must be passed in.
    
    In the last method in the example above, since the method can optionally 
    take an integer value both sets of valid parameter lists should be
    provided.
    
    Valid types that can be checked in the signature and their corresponding
    Python types::

        'string' - str
        'array' - list
        'boolean' - bool
        'int' - int
        'double' - float
        'struct' - dict
        'dateTime.iso8601' - xmlrpclib.DateTime
        'base64' - xmlrpclib.Binary
    
    The class variable ``allow_none`` is passed to xmlrpclib.dumps; enabling it
    allows translating ``None`` to XML (an extension to the XML-RPC
    specification)

    Note::

        Requiring a signature is optional.
    """
    allow_none = False
    max_body_length = 4194304

    def _get_method_args(self):
        return self.rpc_kargs

    def __call__(self, environ, start_response):
        """Parse an XMLRPC body for the method, and call it with the 
        appropriate arguments"""
        # Pull out the length, return an error if there is no valid
        # length or if the length is larger than the max_body_length.
        length = environ.get('CONTENT_LENGTH')
        if length:
            length = int(length)
        else:
            # No valid Content-Length header found
            log.debug("No Content-Length found, returning 411 error")
            abort(411)
        if length > self.max_body_length or length == 0:
            log.debug("Content-Length larger than max body length. Max: %s,"
                      " Sent: %s. Returning 413 error", self.max_body_length, 
                      length)
            abort(413, "XML body too large")

        body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
        rpc_args, orig_method = xmlrpclib.loads(body)

        method = self._find_method_name(orig_method)
        log.debug("Looking for XMLRPC method called: %s", method)
        if not hasattr(self, method):
            log.debug("No method found, returning xmlrpc fault")
            return xmlrpc_fault(0, "No method by that name")(environ, start_response)

        func = getattr(self, method)

        # Signature checking for params
        if hasattr(func, 'signature'):
            log.debug("Checking XMLRPC argument signature")
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
                log.debug("Bad argument signature recieved, returning xmlrpc"
                          " fault")
                msg = ("Incorrect argument signature. %s recieved does not "
                       "match %s signature for method %s" % \
                           (params, func.signature, orig_method))
                return xmlrpc_fault(0, msg)(environ, start_response)

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
        status = []
        headers = []
        def change_content(new_status, new_headers):
            status.append(new_status)
            headers.extend(new_headers)
        output = WSGIController.__call__(self, environ, change_content)
        replace_header(headers, 'Content-Type', 'text/xml')
        start_response(status[0], headers)
        return output

    def _dispatch_call(self):
        """Dispatch the call to the function chosen by __call__"""
        raw_response = self._inspect_call(self._func)
        if not isinstance(raw_response, xmlrpclib.Fault):
            raw_response = (raw_response,)

        response = xmlrpclib.dumps(raw_response, methodresponse=True,
                                   allow_none=self.allow_none)
        return WSGIResponse(response)

    def _find_method_name(self, name):
        """Locate a method in the controller by the appropriate name
        
        By default, this translates method names like 'system.methodHelp' into
        'system_methodHelp'.
        """
        return name.replace('.', '_')

    def _publish_method_name(self, name):
        """Translate an internal method name to a publicly viewable one
        
        By default, this translates internal method names like 'blog_view' into
        'blog.view'.
        """
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
    system_listMethods.signature = [['array']]

    def system_methodSignature(self, name):
        """Returns an array of array's for the valid signatures for a method.

        The first value of each array is the return value of the method. The
        result is an array to indicate multiple signatures a method may be
        capable of.
        """
        name = self._find_method_name(name)
        if hasattr(self, name):
            method = getattr(self, name)
            if hasattr(method, 'signature'):
                return getattr(method, 'signature')
            else:
                return ''
        else:
            return xmlrpclib.Fault(0, 'No such method name')
    system_methodSignature.signature = [['array', 'string'],
                                        ['string', 'string']]

    def system_methodHelp(self, name):
        """Returns the documentation for a method"""
        name = self._find_method_name(name)
        if hasattr(self, name):
            method = getattr(self, name)
            help = getattr(method, 'help', None) or method.__doc__
            help = trim(help)
            sig = getattr(method, 'signature', None)
            if sig:
                help += "\n\nMethod signature: %s" % sig
            return help
        return xmlrpclib.Fault(0, "No such method name")
    system_methodHelp.signature = [['string', 'string']]

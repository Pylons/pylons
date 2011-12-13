"""The base WSGI JSONRPCController"""
import inspect
import json
import logging
import types
import urllib

from paste.response import replace_header
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, Response

__all__ = ['JSONRPCController', 'JSONRPCError',
           'JSONRPC_PARSE_ERROR',
           'JSONRPC_INVALID_REQUEST',
           'JSONRPC_METHOD_NOT_FOUND',
           'JSONRPC_INVALID_PARAMS',
           'JSONRPC_INTERNAL_ERROR']

log = logging.getLogger(__name__)

JSONRPC_VERSION = '2.0'


class JSONRPCError(BaseException):

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.data = None

    def __str__(self):
        return str(self.code) + ': ' + self.message

    def as_dict(self):
        """Return a dictionary representation of this object for
        serialization in a JSON-RPC response."""
        error = dict(code=self.code,
                     message=self.message)
        if self.data:
            error['data'] = self.data

        return error


JSONRPC_PARSE_ERROR = JSONRPCError(-32700, "Parse error")
JSONRPC_INVALID_REQUEST = JSONRPCError(-32600, "Invalid Request")
JSONRPC_METHOD_NOT_FOUND = JSONRPCError(-32601, "Method not found")
JSONRPC_INVALID_PARAMS = JSONRPCError(-32602, "Invalid params")
JSONRPC_INTERNAL_ERROR = JSONRPCError(-32603, "Internal error")
_reserved_errors = dict(parse_error=JSONRPC_PARSE_ERROR,
                        invalid_request=JSONRPC_INVALID_REQUEST,
                        method_not_found=JSONRPC_METHOD_NOT_FOUND,
                        invalid_params=JSONRPC_INVALID_PARAMS,
                        internal_error=JSONRPC_INTERNAL_ERROR)


def jsonrpc_error(req_id, error):
    """Generate a Response object with a JSON-RPC error body. Used to
    raise top-level pre-defined errors that happen outside the
    controller."""
    if error in _reserved_errors:
        err = _reserved_errors[error]
        return Response(body=json.dumps(dict(jsonrpc=JSONRPC_VERSION,
                                             id=req_id,
                                             error=err.as_dict())))


class JSONRPCController(WSGIController):
    """
    A WSGI-speaking JSON-RPC 2.0 controller class

    See the specification:
    `<http://groups.google.com/group/json-rpc/web/json-rpc-2-0>`.

    Many parts of this controller are modelled after XMLRPCController
    from Pylons 0.9.7

    Valid controller return values should be json-serializable objects.

    Sub-classes should catch their exceptions and raise JSONRPCError
    if they want to pass meaningful errors to the client. Unhandled
    errors should be caught and return JSONRPC_INTERNAL_ERROR to the
    client.

    Parts of the specification not supported (yet):
     - Notifications
     - Batch
    """

    def _get_method_args(self):
        """Return `self._rpc_args` to dispatched controller method
        chosen by __call__"""
        return self._rpc_args

    def __call__(self, environ, start_response):
        """Parse the request body as JSON, look up the method on the
        controller and if it exists, dispatch to it.
        """
        length = 0
        if 'CONTENT_LENGTH' not in environ:
            log.debug("No Content-Length")
            abort(411)
        else:
            if environ['CONTENT_LENGTH'] == '':
                abort(411)
            length = int(environ['CONTENT_LENGTH'])
            log.debug('Content-Length: %s', length)
        if length == 0:
            log.debug("Content-Length is 0")
            abort(411)

        raw_body = environ['wsgi.input'].read(length)
        json_body = json.loads(urllib.unquote_plus(raw_body))

        self._req_id = json_body['id']
        self._req_method = json_body['method']
        self._req_params = json_body['params']
        log.debug('id: %s, method: %s, params: %s',
                  self._req_id,
                  self._req_method,
                  self._req_params)

        self._error = None
        try:
            self._func = self._find_method()
        except AttributeError:
            err = jsonrpc_error(self._req_id, 'method_not_found')
            return err(environ, start_response)

        # now that we have a method, make sure we have enough
        # parameters and pass off control to the controller.
        if not isinstance(self._req_params, dict):
            # JSON-RPC version 1 request.
            arglist = inspect.getargspec(self._func)[0][1:]
            if len(self._req_params) < len(arglist):
                err = jsonrpc_error(self._req_id, 'invalid_params')
                return err(environ, start_response)
            else:
                kargs = dict(zip(arglist, self._req_params))
        else:
            # JSON-RPC version 2 request.  Params may be default, and
            # are already a dict, so skip the parameter length check here.
            kargs = self._req_params

        # XX Fix this namespace clash. One cannot use names below as
        # method argument names as this stands!
        kargs['action'], kargs['environ'] = self._req_method, environ
        kargs['start_response'] = start_response
        self._rpc_args = kargs

        status = []
        headers = []
        exc_info = []

        def change_content(new_status, new_headers, new_exc_info=None):
            status.append(new_status)
            headers.extend(new_headers)
            exc_info.append(new_exc_info)

        output = WSGIController.__call__(self, environ, change_content)
        output = list(output)
        headers.append(('Content-Length', str(len(output[0]))))
        replace_header(headers, 'Content-Type', 'application/json')
        start_response(status[0], headers, exc_info[0])

        return output

    def _dispatch_call(self):
        """Implement dispatch interface specified by WSGIController"""
        try:
            raw_response = self._inspect_call(self._func)
        except JSONRPCError, e:
            self._error = e.as_dict()
        except TypeError, e:
            # Insufficient args in an arguments dict v2 call.
            if 'takes at least' in str(e):
                err = _reserved_errors['invalid_params']
                self._error = err.as_dict()
            else:
                raise
        except Exception, e:
            log.debug('Encountered unhandled exception: %s', repr(e))
            err = _reserved_errors['internal_error']
            self._error = err.as_dict()

        response = dict(jsonrpc=JSONRPC_VERSION,
                        id=self._req_id)
        if self._error is not None:
            response['error'] = self._error
        else:
            response['result'] = raw_response

        try:
            return json.dumps(response)
        except TypeError, e:
            log.debug('Error encoding response: %s', e)
            err = _reserved_errors['internal_error']
            return json.dumps(dict(
                    jsonrpc=JSONRPC_VERSION,
                    id=self._req_id,
                    error=err.as_dict()))

    def _find_method(self):
        """Return method named by `self._req_method` in controller if able"""
        log.debug('Trying to find JSON-RPC method: %s', self._req_method)
        if self._req_method.startswith('_'):
            raise AttributeError("Method not allowed")

        try:
            func = getattr(self, self._req_method, None)
        except UnicodeEncodeError:
            # XMLRPCController catches this, not sure why.
            raise AttributeError("Problem decoding unicode in requested "
                                 "method name.")

        if isinstance(func, types.MethodType):
            return func
        else:
            raise AttributeError("No such method: %s" % self._req_method)

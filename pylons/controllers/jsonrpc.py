"""The base WSGI JSONRPCController"""
import inspect
import json
import logging
import types
import urllib

from paste.response import replace_header
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, Response

__all__ = ['JSONRPCController', 'JSONRPCError']

log = logging.getLogger(__name__)


class JSONRPCError(BaseException):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


def jsonrpc_error(req_id, message):
    """Generate a Response object with a JSON-RPC error body"""
    jrpc_err = JSONRPCError(message)
    return Response(body=json.dumps(dict(
                id=req_id,
                result=None,
                error=str(jrpc_err))))

class JSONRPCController(WSGIController):
    """
    A WSGI-speaking JSON-RPC controller class

    See the specification:
    <http://json-rpc.org/wiki/specification>`.

    Many parts of this controller are modelled after XMLRPCController
    from Pylons 0.9.7

    Valid controller return values should be json-serializable objects.

    Sub-classes should catch their exceptions and raise JSONRPCError
    if they want to pass meaningful errors to the client.

    Parts of the specification not supported (yet):
     - Notifications
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
        if not environ.has_key('CONTENT_LENGTH'):
            log.debug("No Content-Length")
            abort(411)
        else:
            length = int(environ['CONTENT_LENGTH'])
            log.debug('Content-Length: %s', length)
        if length == 0:
            log.debug("Content-Length is 0")
            abort(413)
 
        raw_body = environ['wsgi.input'].read(length)[0:-1]
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
        except AttributeError, e:
            return jsonrpc_error(self._req_id, str(e))

        # now that we have a method, add self._req_params to
        # self.kargs and dispatch control to WGIController
        arglist = inspect.getargspec(self._func)[0][1:]
        kargs = dict(zip(arglist, self._req_params))
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
        except JSONRPCError as e:
            self._error = str(e)
        except Exception as e:
            log.debug('Encountered unhandled exception: %s', repr(e))
            json_exc = JSONRPCError('Internal server error')
            self._error = str(json_exc)

        if self._error is not None:
            raw_response = None

        response = dict(
            id=self._req_id,
            result=raw_response,
            error=self._error)

        try:
            return json.dumps(response)
        except TypeError, e:
            log.debug('Error encoding response: %s', e)
            return json.dumps(dict(
                    id=self._req_id,
                    result=None,
                    error="Error encoding response"))

    def _find_method(self):
        """Return method named by `self._req_method` in controller if able"""
        log.debug('Trying to find JSON-RPC method: %s', self._req_method)
        if self._req_method.startswith('_'):
            raise AttributeError, "Method not allowed"

        try:
            func = getattr(self, self._req_method, None)
        except UnicodeEncodeError:
            # XMLRPCController catches this, not sure why.
            raise AttributeError, ("Problem decoding unicode in requested "
                                   "method name.")

        if isinstance(func, types.MethodType):
            return func
        else:
            raise AttributeError, "No such method: %s" % self._req_method

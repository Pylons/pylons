"""Pylons Decorators: ``jsonify``, ``validate``, REST, and Cache decorators"""
import sys
import warnings
import logging
log = logging.getLogger('pylons.decorators')

import simplejson as json
from decorator import decorator

from paste.util.multidict import MultiDict
import formencode.api as api
import formencode.variabledecode as variabledecode
from formencode import htmlfill

import pylons

def jsonify(func, *args, **kwargs):
    """Action decorator that formats output for JSON
    
    Given a function that will return content, this decorator will
    turn the result into JSON, with a content-type of 'text/javascript'
    and output it.
    """
    response = pylons.Response()
    response.headers['Content-Type'] = 'text/javascript'
    data = func(*args, **kwargs)
    if isinstance(data, list):
        msg = "JSON responses with Array envelopes are susceptible to " \
              "cross-site data leak attacks, see " \
              "http://pylonshq.com/warnings/JSONArray"
        warnings.warn(msg, Warning, 2)
        log.warning(msg)
    response.content.append(json.dumps(data))
    log.debug("Returning JSON wrapped action output.")
    return response
jsonify = decorator(jsonify)

def validate(schema=None, validators=None, form=None, variable_decode=False,
             dict_char='.', list_char='-', post_only=True):
    """Validate input either for a FormEncode schema, or individual validators
    
    Given a form schema or dict of validators, validate will attempt to
    validate the schema or validator list as long as a POST request is made. No
    validation is performed on GET requests.
    
    If validation was succesfull, the valid result dict will be saved
    as ``self.form_result``. Otherwise, the action will be re-run as if it was
    a GET, and the output will be filled by FormEncode's htmlfill to fill in
    the form field errors.
    
    If you'd like validate to also check GET (query) variables (**not** GET
    requests!) during its validation, set the ``post_only`` keyword argument 
    to False.
    
    .. warning::
        ``post_only`` applies to *where* the arguments to be validated come 
        from. The validate decorator *only* validates during a POST, it does
        *not* validate during a GET request. 
    
    Example:
    
    .. code-block:: Python
        
        class SomeController(BaseController):
            
            def create(self, id):
                return render_response('/myform.myt')
            
            @validate(schema=model.forms.myshema(), form='create')
            def update(self, id):
                # Do something with self.form_result
                pass
    """
    def wrapper(func, self, *args, **kwargs):
        """Decorator Wrapper function"""
        errors = {}
        if not pylons.request.method == 'POST':
            log.debug("Method was not a form post, validate skipped.")
            return func(self, *args, **kwargs)
        if post_only:
            params = pylons.request.POST.copy()
        else:
            params = pylons.request.params.copy()
        if variable_decode:
            log.debug("Running variable_decode on params.")
            decoded = variabledecode.variable_decode(params, dict_char,
                                                     list_char)
        else:
            decoded = params

        if schema:
            log.debug("Validating against a schema.")
            try:
                self.form_result = schema.to_python(decoded)
            except api.Invalid, e:
                errors = e.unpack_errors(variable_decode, dict_char, list_char)
        if validators:
            log.debug("Validating against provided validators.")
            if isinstance(validators, dict):
                if not hasattr(self, 'form_result'):
                    self.form_result = {}
                for field, validator in validators.iteritems():
                    try:
                        self.form_result[field] = \
                            validator.to_python(decoded[field] or None)
                    except api.Invalid, error:
                        errors[field] = error
        if errors:
            log.debug("Errors found in validation, parsing form with htmlfill for errors.")
            pylons.request.environ['REQUEST_METHOD'] = 'GET'
            pylons.request.environ['pylons.routes_dict']['action'] = form
            response = self._dispatch_call()
            form_content = ''.join(response.content)
            if isinstance(params, MultiDict):
                # Passing raw string form values to htmlfill: Ensure
                # form_content and FormEncode's errors dict are also raw
                # strings so htmlfill can safely combine them
                encoding = determine_response_charset(response)
                # WSGIResponse's content may (unlikely) be unicode
                if isinstance(form_content, unicode):
                    form_content = form_content.encode(encoding)
                # FormEncode>=0.7 error strings are unicode (due to being
                # localized via ugettext)
                for key, value in errors.iteritems():
                    if isinstance(value, unicode):
                        errors[key] = value.encode(encoding)
            elif not isinstance(form_content, unicode):
                # Passing unicode form values to htmlfill: decode the response
                # to unicode so htmlfill can safely combine the two
                encoding = determine_response_charset(response)
                form_content = form_content.decode(encoding, response.errors)
            response.content = [htmlfill.render(form_content, params, errors)]
            return response
        return func(self, *args, **kwargs)
    return decorator(wrapper)

def determine_response_charset(response):
    """Determine the charset of the specified Response object, returning the
    default system encoding when none is set"""
    charset = response.determine_charset()
    if charset is None:
        charset = sys.getdefaultencoding()
    log.debug("Determined result charset to be: %s", charset)
    return charset

__all__ = ['jsonify', 'validate']

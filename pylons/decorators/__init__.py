"""Pylons Decorators: ``jsonify``, ``validate``, REST, and Cache decorators"""
import simplejson as json
import sys
from paste.util.multidict import UnicodeMultiDict

from decorator import decorator

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
    response.content.append(json.dumps(func(*args, **kwargs)))
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
            return func(self, *args, **kwargs)
        if post_only:
            params = pylons.request.POST.copy()
        else:
            params = pylons.request.params.copy()
        if variable_decode:
            decoded = variabledecode.variable_decode(params, dict_char,
                                                     list_char)
        else:
            decoded = params

        if schema:
            try:
                self.form_result = schema.to_python(decoded)
            except api.Invalid, e:
                errors = e.unpack_errors(variable_decode, dict_char, list_char)
        if validators:
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
            pylons.request.environ['REQUEST_METHOD'] = 'GET'
            pylons.request.environ['pylons.routes_dict']['action'] = form
            response = self._dispatch_call()
            form_content = ''.join(response.content)
            if isinstance(params, UnicodeMultiDict) and \
                    not isinstance(form_content, unicode):
                # Passing unicode form values to htmlfill: decode the response
                # to unicode so htmlfill can safely combine the two
                encoding = response.determine_charset()
                if encoding is None:
                    encoding = sys.getdefaultencoding()
                form_content = form_content.decode(encoding, response.errors)
            response.content = [htmlfill.render(form_content, params, errors)]
            return response
        return func(self, *args, **kwargs)
    return decorator(wrapper)

__all__ = ['jsonify', 'validate']

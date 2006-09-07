"""Custom Decorators, currently ``jsonify``, ``validate``, and 2 REST decorators"""
import types
import simplejson as json
import formencode.api as api
from formencode import htmlfill
import formencode.variabledecode as variabledecode
import pylons
from pylons.decorator import decorator
import rest

def jsonify(func, *args, **kw):
    """Action decorator that formats output for JSON
    
    Given a function that will return content, this decorator will
    turn the result into JSON, with a content-type of 'text/javascript'
    and output it.
    
    """
    response = pylons.Response()
    response.headers['Content-Type'] = 'text/javascript'
    response.content.append(json.dumps(func(*args, **kw)))
    return response
jsonify = decorator(jsonify)

def validate(schema=None, validators=None, form=None, variable_decode=False):
    """Validate input either for a FormEncode schema, or individual validators
    
    Given a form schema or dict of validators, validate will attempt to validate
    the schema or validator list as long as a POST request is made. No 
    validation is performed on GET requests.
    
    If validation was succesfull, the valid result dict will be saved
    as ``self.form_result``. Otherwise, the action will be re-run as if it was a
    GET, and the output will be filled by FormEncode's htmlfill to fill in the
    form field errors.
    
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
    def validate(func, self, *args, **kwargs):
        defaults, errors = {}, {}
        if not pylons.request.method == 'POST':
            return func(self, *args, **kwargs)
        postvars = pylons.request.POST.copy()
        if variable_decode:
            postvars = variabledecode.variable_decode(postvars)
        
        defaults.update(postvars)
        if schema:
            try:
                self.form_result = schema.to_python(defaults)
            except api.Invalid, e:
                errors = e.unpack_errors(variable_decode)
        if validators:
            if isinstance(validators, dict):
                if not hasattr(self, 'form_result'):
                    self.form_result = {}
                for field, validator in validators.iteritems():
                    try:
                        self.form_result[field] = \
                            validator.to_python(defaults[field] or None)
                    except api.Invalid, error:
                        errors[field] = error
        if errors:
            pylons.request.environ['REQUEST_METHOD'] = 'GET'
            pylons.request.environ['pylons.routes_dict']['action'] = form
            response = self._dispatch_call()
            form_content = "".join(response.content)
            response.content = [htmlfill.render(form_content, defaults, errors)]
            return response
        return func(self, *args, **kwargs)
    return decorator(validate)

__all__ = ['jsonify', 'validate', 'rest']

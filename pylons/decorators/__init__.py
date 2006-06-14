"""Custom Decorators, currently ``jsonify``, ``validate``, and 2 REST decorators"""
import simplejson as json
import formencode.api as api
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

def validate(form=None, validators=None):
    """Validate input either for a FormEncode schema, or individual validators
    
    Given a form schema or dict of validators, validate will attempt to validate
    the schema or validator list. Errors will be saved to ``c.errors``, and the
    defaults used will be saved as ``c.defaults``. Testing to see if the validation
    was successful should be done on ``self.valid`` which will return True or False.
    
    If validation was succesfull, the valid result dict will be saved as
     ``self.form_results``.
    
    Example::
        
        class SomeController(BaseController):
            
            @validate(form=model.forms.myshema())
            def comment(self, id):
                if self.valid:
                    # Do something with self.form_results
                else:
                    # Render the new form, using pylons.helpers.formfill helps
                    return render_response('/myform.myt')
    
    **Note**: For the curious, variables only useful in the controller are attached
    to it, while variables useful during rendering are attached to ``c``.
    
    """
    def validate(func, self, *args, **kwargs):
        self.valid = False
        pylons.c.defaults, pylons.c.errors = {}, {}
        if not pylons.request.method == 'POST':
            return func(self, *args, **kwargs)
        for key in pylons.request.POST.keys():
            pylons.c.defaults[key] = pylons.request.POST[key]
        if form:
            try:
                self.form_result = form.to_python(pylons.c.defaults)
            except api.Invalid, e:
                pylons.c.errors = e.unpack_errors()
        if validators:
            if isinstance(validators, dict):
                for field, validator in validators.iteritems():
                    try:
                        self.form_result[field] = \
                            validator.to_python(pylons.c.defaults[field] or None)
                    except api.Invalid, error:
                        pylons.c.errors[field] = error
        if not pylons.c.errors:
            self.valid = True
        return func(self, *args, **kwargs)
    return decorator(validate)

__all__ = ['jsonify', 'validate', 'rest']

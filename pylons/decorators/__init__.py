"""Custom Decorators, currently ``jsonify``"""
import simplejson as json
import formencode.api as api
import pylons
from pylons.decorator import decorator
import rest

def jsonify(func):
    """Action decorator that formats output for JSON
    
    Given a function that will return content, this decorator will
    turn the result into JSON, with a content-type of 'text/javascript'
    and output it.
    
    """
    def entangle(func):
        def json(func, *args, **kw):
            response = pylons.Response()
            response.headers['Content-Type'] = 'text/javascript'
            response.content.append(json.dumps(func(*args, **kw)))
            return response
        return json
    return decorator(entangle)

def validate(form=None, validators=None):
    """Validate input either for a FormEncode schema, or individual validators
    
    Given a form schema or list of validators, validate will attempt to validate
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
    
    """
    def entangle(func):
        def validate(func, self, *args, **kwargs):
            self.valid = False
            c = pylons.c
            params = {}
            for key in pylons.request.POST.keys():
                params[key] = pylons.request.POST[key]
            c.errors, c.defaults = {}, params
            if not c.defaults:
                return func(self, *args, **kwargs)
            try:
                self.form_result = form.to_python(c.defaults)
            except api.Invalid, e:
                c.errors = e.unpack_errors()
            if not c.errors:
                self.valid = True
            return func(self, *args, **kwargs)
        return validate
    return decorator(entangle)
    
__all__ = ['jsonify']

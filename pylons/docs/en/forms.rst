.. _forms:

===========
Forms
===========

The basics
==========

When a user submits a form on a website the data is submitted to the URL specified in the `action` attribute of the `<form>` tag. The data can be submitted either via HTTP `GET` or `POST` as specified by the `method` attribute of the `<form>` tag. If your form doesn't specify an `action`, then it's submitted to the current URL, generally you'll want to specify an `action`. When a file upload field such as `<input type="file" name="file" />` is present, then the HTML `<form>` tag must also specify `enctype="multipart/form-data"` and `method` must be `POST`. 


Getting Started 
=============== 

Add two actions that looks like this: 

.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    def email(self): 
        return 'Your email is: %s' % request.params['email'] 

Add a new template called `form.mako` in the `templates` directory that contains the following: 

.. code-block:: html 

    <form name="test" method="GET" action="/hello/email"> 
    Email Address: <input type="text" name="email" /> 
    <input type="submit" name="submit" value="Submit" /> 
    </form> 

If the server is still running (see the :ref:`Getting Started Guide <getting_started>`) you can visit http://localhost:5000/hello/form and you will see the form. Try entering the email address `test@example.com` and clicking Submit. The URL should change to ``http://localhost:5000/hello/email?email=test%40example.com`` and you should see the text `Your email is test@example.com`. 

In Pylons all form variables can be accessed from the :data:`request.params` object which behaves like a dictionary. The keys are the names of the fields in the form and the value is a string with all the characters entity decoded. For example note how the `@` character was converted by the browser to `%40` in the URL and was converted back ready for use in :data:`request.params`. 

.. Note:: `request` and `response` are objects from the `WebOb` library.  Full documentation on their attributes and methods is `here <http://pythonpaste.org/webob/>`_.

If you have two fields with the same name in the form then using the dictionary interface will return the first string. You can get all the strings returned as a list by using the `.getall()` method. If you only expect one value and want to enforce this you should use `.getone()` which raises an error if more than one value with the same name is submitted. 

By default if a field is submitted without a value, the dictionary interface returns an empty string. This means that using `.get(key, default)` on `request.params` will only return a default if the value was not present in the form. 


POST vs GET and the Re-Submitted Data Problem 
--------------------------------------------- 

If you change the `form.mako` template so that the method is `POST` and you re-run the example you will see the same message is displayed as before. However, the URL displayed in the browser is simply http://localhost:5000/hello/email without the query string. The data is sent in the body of the request instead of the URL, but Pylons makes it available in the same way as for GET requests through the use of `request.params`. 

.. note:: 

    If you are writing forms that contain password fields you should usually use POST to prevent the password being visible to anyone who might be looking at the user's screen. 

When writing form-based applications you will occasionally find users will press refresh immediately after submitting a form. This has the effect of repeating whatever actions were performed the first time the form was submitted but often the user will expect that the current page be shown again. If your form was submitted with a POST, most browsers will display a message to the user asking them if they wish to re-submit the data, this will not happen with a GET so POST is preferable to GET in those circumstances. 

Of course, the best way to solve this issue is to structure your code differently so: 

.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    def email(self): 
        # Code to perform some action based on the form data 
        # ... 
        redirect(url(controller='home', action='result'))

    def result(self): 
        return 'Your data was successfully submitted' 

In this case once the form is submitted the data is saved and an HTTP redirect occurs so that the browser redirects to http://localhost:5000/hello/result. If the user then refreshes the page, it simply redisplays the message rather than re-performing the action. 


Using the Helpers 
================= 

Creating forms can also be done using WebHelpers, which comes with Pylons. Here is the same form created in the previous section but this time using the helpers: 

.. code-block:: html+mako 

    ${h.form(h.url(action='email'), method='get')} 
    Email Address: ${h.text('email')} 
    ${h.submit('Submit')} 
    ${h.end_form()} 

Before doing this you'll have to import the helpers you want to use into your
project's `lib/helpers.py` file; then they'll be available under Pylons' ``h``
global.  Most projects will want to import at least these:

.. code-block:: python

   from webhelpers.html import escape, HTML, literal, url_escape
   from webhelpers.html.tags import *

There are many other helpers for text formatting, container objects,
statistics, and for dividing large query results into pages.  See the
:mod:`WebHelpers documentation <webhelpers>` to choose the helpers you'll need.


.. _file_uploads:

File Uploads 
============ 
File upload fields are created by using the `file` input field type. The `file_field` helper provides a shortcut for creating these form fields: 

.. code-block:: mako 

    ${h.file_field('myfile')} 

The HTML form must have its `enctype` attribute set to `multipart/form-data` to enable the browser to upload the file. The `form` helper's `multipart` keyword argument provides a shortcut for setting the appropriate `enctype` value: 

.. code-block:: html+mako 

    ${h.form(h.url(action='upload'), multipart=True)} 
    Upload file: ${h.file_field('myfile')} <br /> 
    File description: ${h.text_field('description')} <br /> 
    ${h.submit('Submit')} 
    ${h.end_form()} 

When a file upload has succeeded, the `request.POST` (or `request.params`) `MultiDict` will contain a `cgi.FieldStorage` object as the value of the field. 

`FieldStorage` objects have three important attributes for file uploads: 

`filename` 
    The name of file uploaded as it appeared on the uploader's filesystem. 

`file` 
    A file(-like) object from which the file's data can be read: A python `tempfile` or a `StringIO` object. 

`value` 
    The content of the uploaded file, eagerly read directly from the file object. 

The easiest way to gain access to the file's data is via the `value` attribute: it returns the entire contents of the file as a string: 

.. code-block:: python 

    def upload(self): 
        myfile = request.POST['myfile'] 
        return 'Successfully uploaded: %s, size: %i, description: %s' % \ 
            (myfile.filename, len(myfile.value), request.POST['description']) 

However reading the entire contents of the file into memory is undesirable, especially for large file uploads. A common means of handling file uploads is to store the file somewhere on the filesystem. The `FieldStorage` typically reads the file onto filesystem, however to a non permanent location, via a python `tempfile` object (though for very small uploads it stores the file in a `StringIO` object instead). 

Python `tempfiles` are secure file objects that are automatically destroyed when they are closed (including an implicit close when the object is garbage collected). One of their security features is that their path cannot be determined: a simple `os.rename` from the `tempfile's` path isn't possible. Alternatively, `shutil.copyfileobj` can perform an efficient copy of the file's data to a permanent location: 

.. code-block:: python 

    permanent_store = '/uploads/' 

    class Uploader(BaseController): 
        def upload(self): 
            myfile = request.POST['myfile'] 
            permanent_file = open(os.path.join(permanent_store, 
                                    myfile.filename.lstrip(os.sep)), 
                                    'w') 

        shutil.copyfileobj(myfile.file, permanent_file) 
        myfile.file.close() 
        permanent_file.close() 

        return 'Successfully uploaded: %s, description: %s' % \ 
            (myfile.filename, request.POST['description']) 

.. warning:: 
    The previous basic example allows any file uploader to overwrite any file in
    the `permanent_store` directory that your web application has permissions
    to.

Also note the use of `myfile.filename.lstrip(os.sep)` here: without it, `os.path.join` is unsafe. `os.path.join` won't join absolute paths (beginning with `os.sep`), i.e. `os.path.join('/uploads/', '/uploaded_file.txt')` == `'/uploaded_file.txt'`. Always check user submitted data to be used with `os.path.join`. 

Validating user input with FormEncode
=====================================

Validation the Quick Way 
------------------------

At the moment you could enter any value into the form and it would be displayed in the message, even if it wasn't a valid email address. In most cases this isn't acceptable since the user's input needs validating. The recommended tool for validating forms in Pylons is `FormEncode <http://www.formencode.org>`_. 

For each form you create you also create a validation schema. In our case this is fairly easy: 

.. code-block:: python 

    import formencode 

    class EmailForm(formencode.Schema): 
        allow_extra_fields = True 
        filter_extra_fields = True 
        email = formencode.validators.Email(not_empty=True) 

.. note:: 

    We usually recommend keeping form schemas together so that you have a single
    place you can go to update them. It's also convenient for inheritance since
    you can make new form schemas that build on existing ones. If you put your
    forms in a `models/form.py` file, you can easily use them throughout your
    controllers as `model.form.EmailForm` in the case shown.

Our form actually has two fields, an email text field and a submit button. If extra fields are submitted FormEncode's default behavior is to consider the form invalid so we specify `allow_extra_fields = True`. Since we don't want to use the values of the extra fields we also specify `filter_extra_fields = True`. The final line specifies that the email field should be validated with an `Email()` validator. In creating the validator we also specify `not_empty=True` so that the email field will require input. 

Pylons comes with an easy to use `validate` decorator, if you wish to use it import it in your `lib/base.py` like this:

.. code-block:: python

    # other imports

    from pylons.decorators import validate
 
Using it in your controller is pretty straight-forward: 

.. code-block:: python 

    # in the controller 

    def form(self): 
        return render('/form.mako') 

    @validate(schema=EmailForm(), form='form') 
    def email(self): 
        return 'Your email is: %s' % self.form_result.get('email') 

Validation only occurs on POST requests so we need to alter our form definition so that the method is a POST: 

.. code-block:: mako 

    ${h.form(h.url(action='email'), method='post')} 

If validation is successful, the valid result dict will be saved as
`self.form_result` so it can be used in the action. Otherwise, the action will
be re-run as if it was a GET request to the controller action specified in
`form`, and the output will be filled by FormEncode's htmlfill to fill in the
form field errors. For simple cases this is really handy because it also avoids
having to write code in your templates to display error messages if they are
present.

This does exactly the same thing as the example above but works with the
original form definition and in fact will work with any HTML form regardless of
how it is generated because the validate decorator uses `formencode.htmlfill`
to find HTML fields and replace them with the values were originally submitted.

.. note:: 

    Python 2.3 doesn't support decorators so rather than using the
    `@validate()` syntax you need to put `email =
    validate(schema=EmailForm(), form='form')(email)` after the email
    function's declaration.


Validation the Long Way 
-----------------------

The `validate` decorator covers up a bit of work, and depending on your needs it's possible you could need direct access to FormEncode abilities it smoothes over. 

Here's the longer way to use the `EmailForm` schema: 

.. code-block:: python 

    # in the controller 

    def email(self): 
        schema = EmailForm() 
        try: 
            form_result = schema.to_python(request.params) 
        except formencode.validators.Invalid, error: 
            return 'Invalid: %s' % error 
        else: 
            return 'Your email is: %s' % form_result.get('email') 

If the values entered are valid, the schema's `to_python()` method returns a
dictionary of the validated and coerced `form_result`. This means that you can
guarantee that the `form_result` dictionary contains values that are valid and
correct Python objects for the data types desired.

In this case the email address is a string so `request.params['email']`
happens to be the same as `form_result['email']`. If our form contained a
field for age in years and we had used a `formencode.validators.Int()`
validator, the value in `form_result` for the age would also be the correct
type; in this case a Python integer.

FormEncode comes with a useful set of validators but you can also easily
create your own. If you do create your own validators you will find it very
useful that all FormEncode schemas' `.to_python()` methods take a second
argument named `state`. This means you can pass the Pylons `c` object
into your validators so that you can set any variables that your validators
need in order to validate a particular field as an attribute of the `c`
object. It can then be passed as the `c` object to the schema as follows:

.. code-block:: python 

    c.domain = 'example.com' 
    form_result = schema.to_python(request.params, c) 

The schema passes `c` to each validator in turn so that you can do things like this: 

.. code-block:: python 

    class SimpleEmail(formencode.validators.Email): 
        def _to_python(self, value, c): 
            if not value.endswith(c.domain): 
                raise formencode.validators.Invalid(
                    'Email addresses must end in: %s' % \ 
                        c.domain, value, c) 
            return formencode.validators.Email._to_python(self, value, c) 

For this to work, make sure to change the `EmailForm` schema you've defined to use the new `SimpleEmail` validator. In other words, 

.. code-block:: python 

    email = formencode.validators.Email(not_empty=True) 
    # becomes: 
    email = SimpleEmail(not_empty=True) 


In reality the invalid error message we get if we don't enter a valid email address isn't very useful. We really want to be able to redisplay the form with the value entered and the error message produced. Replace the line: 

.. code-block:: python 

    return 'Invalid: %s' % error 

with the lines: 

.. code-block:: python 

    c.form_result = error.value 
    c.form_errors = error.error_dict or {} 
    return render('/form.mako') 

Now we will need to make some tweaks to `form.mako`. Make it look like this: 

.. code-block:: html+mako 

    ${h.form(h.url(action='email'), method='get')} 

    % if c.form_errors: 
    <h2>Please correct the errors</h2> 
    % else: 
    <h2>Enter Email Address</h2> 
    % endif 

    % if c.form_errors: 
    Email Address: ${h.text_field('email', value=c.form_result['email'] or '')} 
    <p>${c.form_errors['email']}</p> 
    % else: 
    Email Address: ${h.text_field('email')} 
    % endif 

    ${h.submit('Submit')} 
    ${h.end_form()} 

Now when the form is invalid the `form.mako` template is re-rendered with the error messages. 


Other Form Tools 
================ 

If you are going to be creating a lot of forms you may wish to consider using `FormBuild <http://formbuild.org>`_ to help create your forms. To use it you create a custom Form object and use that object to build all your forms. You can then use the API to modify all aspects of the generation and use of all forms built with your custom Form by modifying its definition without any need to change the form templates. 

Here is an one example of how you might use it in a controller to handle a form submission: 

.. code-block:: python 

    # in the controller 

    def form(self): 
        results, errors, response = formbuild.handle( 
            schema=Schema(), # Your FormEncode schema for the form 
                             # to be validated 
            template='form.mako', # The template containg the code 
                                  # that builds your form 
            form=Form # The FormBuild Form definition you wish to use 
        )
        if response: 
            # The form validation failed so re-display 
            # the form with the auto-generted response 
            # containing submitted values and errors or 
            # do something with the errors 
            return response 
        else: 
            # The form validated, do something useful with results. 
            ... 

Full documentation of all features is available in the `FormBuild manual <http://formbuild.org/manual.html>`_ which you should read before looking at `Using FormBuild in Pylons <http://formbuild.org/pylons.html>`_ 

Looking forward it is likely Pylons will soon be able to use the TurboGears widgets system which will probably become the recommended way to build forms in Pylons. 

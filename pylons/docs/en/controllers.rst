.. _controllers:

===========
Controllers
===========

.. image:: _static/pylon2.jpg
   :alt: 
   :align: left
   :height: 450px
   :width: 368px

In the :term:`MVC` paradigm the *controller* interprets the inputs, commanding
the model and/or the view to change as appropriate. Under Pylons, this concept
is extended slightly in that a Pylons controller is not directly interpreting
the client's request, but is acting to determine the appropriate way to
assemble data from the model, and render it with the correct template.

The controller interprets requests from the user and calls portions of the model and view as necessary to fulfill the request. So when the user clicks a Web link or submits an HTML form, the controller itself doesn’t output anything or perform any real processing. It takes the request and determines which model components to invoke and which formatting to apply to the resulting data.

Pylons uses a class, where the superclass provides the :term:`WSGI` interface
and the subclass implements the application-specific controller logic.

The Pylons WSGI Controller handles incoming web requests that are dispatched from the Pylons WSGI application :class:`~pylons.wsgiapp.PylonsApp`.

These requests result in a new instance of the :class:`~pylons.controllers.core.WSGIController` being created, which is then called with the dict options from the Routes match. The standard WSGI response is then returned with start_response called as per the WSGI spec.

Since Pylons controllers are actually called with the WSGI interface, normal WSGI applications can also be Pylons ‘controllers’.

Standard Controllers
====================

Standard Controllers intended for subclassing by web developers

Keeping methods private
-----------------------

The default route maps any controller and action, so you will likely want to
prevent some controller methods from being callable from a URL.

Pylons uses the default Python convention of private methods beginning with
``_``. To hide a method ``edit_generic`` in this class, just changing its name
to begin with ``_`` will be sufficient:

.. code-block:: python

    class UserController(BaseController):
        def index(self):
            return "This is the index."

        def _edit_generic(self):
            """I can't be called from the web!"""
            return True

Special methods
---------------

Special controller methods you may define:

``__before__``
    This method is called before your action is, and should be used for
    setting up variables/objects, restricting access to other actions,
    or other tasks which should be executed before the action is called.

``__after__``
    This method is called after the action is, unless an unexpected
    exception was raised. Subclasses of
    :class:`~webob.exc.HTTPException` (such as those raised by
    ``redirect_to`` and ``abort``) are expected; e.g. ``__after__``
    will be called on redirects.
    
Adding Controllers dynamically
------------------------------

It is possible for an application to add controllers without restarting the application. This requires telling Routes to re-scan the controllers directory.

New controllers may be added from the command line with the paster command (recommended as that also creates the test harness file), or any other means of creating the controller file.

For Routes to become aware of new controllers present in the controller directory, an internal flag is toggled to indicate that Routes should rescan the directory:

.. code-block:: python

    from routes import request_config

    mapper = request_config().mapper
    mapper._created_regs = False


On the next request, Routes will rescan the controllers directory and those routes that use the ``:controller`` dynamic part of the path will be able to match the new controller.

Customizing the Controller Name
-------------------------------

By default, Pylons looks for a controller named 'Something'Controller. This
naming scheme can be overridden by supplying an optional module-level variable
called ``__controller__`` to indicate the desired controller class::
    
    import logging

    from pylons import request, response, session, tmpl_context as c
    from pylons.controllers.util import abort, redirect_to

    from helloworld.lib.base import BaseController, render

    log = logging.getLogger(__name__)
    
    __controller__ = 'Hello'

    class Hello(BaseController):

        def index(self):
            # Return a rendered template
            #return render('/hello.mako')
            # or, return a string
            return 'Hello World'
    


Attaching WSGI apps
-------------------

.. note::

    This recipe assumes a basic level of familiarity with the WSGI Specification (PEP 333)

WSGI runs deep through Pylons, and is present in many parts of the architecture. Since Pylons controllers are actually called with the WSGI interface, normal WSGI applications can also be Pylons 'controllers'. 

Optionally, if a full WSGI app should be mounted and handle the remainder of the URL, Routes can automatically move the right part of the URL into the :envvar:`SCRIPT_NAME`, so that the WSGI application can properly handle its :envvar:`PATH_INFO` part.

This recipe will demonstrate adding a basic WSGI app as a Pylons controller. 

Create a new controller file in your Pylons project directory:

.. code-block:: python

    $ paster controller wsgiapp

This sets up the basic imports that you may want available when using other WSGI applications.

Edit your controller so it looks like this:

.. code-block:: python

    import logging

    from YOURPROJ.lib.base import *

    log = logging.getLogger(__name__)

    def WsgiappController(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ["Hello World"]

When hooking up other WSGI applications, they will expect the part of the URL that was used to get to this controller to have been moved into :envvar:`SCRIPT_NAME`. :mod:`Routes <routes>` can properly adjust the environ if a map route for this controller is added to the :file:`config/routing.py` file:

.. code-block:: python

    # CUSTOM ROUTES HERE

    # Map the WSGI application
    map.connect('wsgiapp/{path_info:.*}', controller='wsgiapp')


By specifying the ``path_info`` dynamic path, Routes will put everything leading up to the ``path_info`` in the :envvar:`SCRIPT_NAME` and the rest will go in the :envvar:`PATH_INFO`.


Using the WSGI Controller to provide a WSGI service
===================================================

The Pylons WSGI Controller
--------------------------

Pylons' own WSGI Controller follows the WSGI spec for calling and return
values

The Pylons WSGI Controller handles incoming web requests that are 
dispatched from ``PylonsApp``. These requests result in a new
instance of the ``WSGIController`` being created, which is then called
with the dict options from the Routes match. The standard WSGI
response is then returned with :meth:`start_response` called as per
the WSGI spec.

WSGIController methods
----------------------


Special ``WSGIController`` methods you may define:

``__before__``
    This method will be run before your action is, and should be
    used for setting up variables/objects, restricting access to
    other actions, or other tasks which should be executed before
    the action is called.
``__after__``
    Method to run after the action is run. This method will
    *always* be run after your method, even if it raises an
    Exception or redirects.
    
Each action to be called is inspected with :meth:`_inspect_call` so
that it is only passed the arguments in the Routes match dict that
it asks for. The arguments passed into the action can be customized
by overriding the :meth:`_get_method_args` function which is
expected to return a dict.

In the event that an action is not found to handle the request, the
Controller will raise an "Action Not Found" error if in debug mode,
otherwise a ``404 Not Found`` error will be returned.

.. _rest_controller:

Using the REST Controller with a RESTful API
============================================

Using the paster restcontroller template
----------------------------------------

.. code-block:: bash

    $ paster restcontroller --help

Create a REST Controller and accompanying functional test

The RestController command will create a REST-based Controller file
for use with the :meth:`~routes.base.Mapper.resource`
REST-based dispatching. This template includes the methods that
:meth:`~routes.base.Mapper.resource` dispatches to in
addition to doc strings for clarification on when the methods will
be called.

The first argument should be the singular form of the REST
resource. The second argument is the plural form of the word. If
its a nested controller, put the directory information in front as
shown in the second example below.

Example usage:

.. code-block:: bash

    $ paster restcontroller comment comments
    Creating yourproj/yourproj/controllers/comments.py
    Creating yourproj/yourproj/tests/functional/test_comments.py

If you'd like to have controllers underneath a directory, just
include the path as the controller name and the necessary
directories will be created for you:

.. code-block:: bash

    $ paster restcontroller admin/trackback admin/trackbacks
    Creating yourproj/controllers/admin
    Creating yourproj/yourproj/controllers/admin/trackbacks.py
    Creating yourproj/yourproj/tests/functional/test_admin_trackbacks.py

An Atom-Style REST Controller for Users
---------------------------------------

.. code-block:: python

    # From http://pylonshq.com/pasties/503
    import logging

    from formencode.api import Invalid
    from pylons import url
    from simplejson import dumps

    from restmarks.lib.base import *

    log = logging.getLogger(__name__)

    class UsersController(BaseController):
        """REST Controller styled on the Atom Publishing Protocol"""
        # To properly map this controller, ensure your 
        # config/routing.py file has a resource setup:
        #     map.resource('user', 'users')

        def index(self, format='html'):
            """GET /users: All items in the collection.<br>
                @param format the format passed from the URI.
            """
            #url('users')
            users = model.User.select()
            if format == 'json':
                data = []
                for user in users:
                    d = user._state['original'].data
                    del d['password']
                    d['link'] = url('user', id=user.name)
                    data.append(d)
                response.headers['content-type'] = 'text/javascript'
                return dumps(data)
            else:
                c.users = users
                return render('/users/index_user.mako')

        def create(self):
            """POST /users: Create a new item."""
            # url('users')
            user = model.User.get_by(name=request.params['name'])
            if user:
                # The client tried to create a user that already exists
                abort(409, '409 Conflict', 
                      headers=[('location', url('user', id=user.name))])
            else:
                try:
                    # Validate the data that was sent to us
                    params = model.forms.UserForm.to_python(request.params)
                except Invalid, e:
                    # Something didn't validate correctly
                    abort(400, '400 Bad Request -- %s' % e)
                user = model.User(**params)
                model.objectstore.flush()
                response.headers['location'] = url('user', id=user.name)
                response.status_code = 201
                c.user_name = user.name
                return render('/users/created_user.mako')

        def new(self, format='html'):
            """GET /users/new: Form to create a new item.
                @param format the format passed from the URI.
            """
            # url('new_user')
            return render('/users/new_user.mako')

        def update(self, id):
            """PUT /users/id: Update an existing item.
                @param id the id (name) of the user to be updated
            """
            # Forms posted to this method should contain a hidden field:
            #    <input type="hidden" name="_method" value="PUT" />
            # Or using helpers:
            #    h.form(url('user', id=ID),
            #           method='put')
            # url('user', id=ID)
            old_name = id
            new_name = request.params['name']
            user = model.User.get_by(name=id)

            if user:
                if (old_name != new_name) and model.User.get_by(name=new_name):
                    abort(409, '409 Conflict')
                else:
                    params = model.forms.UserForm.to_python(request.params)
                    user.name = params['name']
                    user.full_name = params['full_name']
                    user.email = params['email']
                    user.password = params['password']
                    model.objectstore.flush()
                    if user.name != old_name:
                        abort(301, '301 Moved Permanently',
                              [('Location', url('users', id=user.name))])
                    else:
                        return

        def delete(self, id):
            """DELETE /users/id: Delete an existing item.
                @param id the id (name) of the user to be updated
            """
            # Forms posted to this method should contain a hidden field:
            #    <input type="hidden" name="_method" value="DELETE" />
            # Or using helpers:
            #    h.form(url('user', id=ID),
            #           method='delete')
            # url('user', id=ID)
            user = model.User.get_by(name=id)
            user.delete()
            model.objectstore.flush()
            return

        def show(self, id, format='html'):
            """GET /users/id: Show a specific item.
                @param id the id (name) of the user to be updated.
                @param format the format of the URI requested.
            """
            # url('user', id=ID)
            user = model.User.get_by(name=id)
            if user:
                if format=='json':
                    data = user._state['original'].data
                    del data['password']
                    data['link'] = url('user', id=user.name)
                    response.headers['content-type'] = 'text/javascript'
                    return dumps(data)
                else:
                    c.data = user
                    return render('/users/show_user.mako')
            else:
                abort(404, '404 Not Found')

        def edit(self, id, format='html'):
            """GET /users/id;edit: Form to edit an existing item.
                @param id the id (name) of the user to be updated.
                @param format the format of the URI requested.
            """
            # url('edit_user', id=ID)
            user = model.User.get_by(name=id)
            if not user:
                abort(404, '404 Not Found')
            # Get the form values from the table
            c.values = model.forms.UserForm.from_python(user.__dict__)
            return render('/users/edit_user.mako')

.. _xmlrpc_controller:

Using the XML-RPC Controller for XML-RPC requests
================================================= 

In order to deploy this controller you will need at least a passing familiarity with XML-RPC itself. We will first review the basics of XML-RPC and then describe the workings of the ``Pylons XMLRPCController``. Finally, we will show an example of how to use the controller to implement a simple web service. 

After you've read this document, you may be interested in reading the companion document: "A blog publishing web service in XML-RPC" which takes the subject further, covering details of the MetaWeblog API (a popular XML-RPC service) and demonstrating how to construct some basic service methods to act as the core of a MetaWeblog blog publishing service. 

A brief introduction to XML-RPC
------------------------------- 

XML-RPC is a specification that describes a Remote Procedure Call (RPC) interface by which an application can use the Internet to execute a specified procedure call on a remote XML-RPC server. The name of the procedure to be called and any required parameter values are "marshalled" into XML. The XML forms the body of a POST request which is despatched via HTTP to the XML-RPC server. At the server, the procedure is executed, the returned value(s) is/are marshalled into XML and despatched back to the application. XML-RPC is designed to be as simple as possible, while allowing complex data structures to be transmitted, processed and returned. 

XML-RPC Controller that speaks WSGI 
-----------------------------------

Pylons uses Python's xmlrpclib library to provide a specialised :class:`XMLRPCController` class that gives you the full range of these XML-RPC Introspection facilities for use in your service methods and provides the foundation for constructing a set of specialised service methods that provide a useful web service --- such as a blog publishing interface. 

This controller handles XML-RPC responses and complies with the `XML-RPC Specification <http://www.xmlrpc.com/spec>`_ as well as the `XML-RPC Introspection <http://scripts.incutio.com/xmlrpc/introspection.html>`_ specification. 

As part of its basic functionality an XML-RPC server provides three standard introspection procedures or "service methods" as they are called. The Pylons :class:`XMLRPCController` class provides these standard service methods ready-made for you: 

* :meth:`system.listMethods` Returns a list of XML-RPC methods for this XML-RPC resource 
* :meth:`system.methodSignature` Returns an array of arrays for the valid signatures for a method. The first value of each array is the return value of the method. The result is an array to indicate multiple signatures a method may be capable of. 
* :meth:`system.methodHelp` Returns the documentation for a method 

By default, methods with names containing a dot are translated to use an underscore. For example, the ``system.methodHelp`` is handled by the method :meth:`system_methodHelp`. 

Methods in the XML-RPC controller will be called with the method given in the XML-RPC body. Methods may be annotated with a signature attribute to declare the valid arguments and return types. 

For example:

.. code-block:: python

    class MyXML(XMLRPCController): 
        def userstatus(self): 
            return 'basic string' 
        userstatus.signature = [['string']] 

        def userinfo(self, username, age=None): 
            user = LookUpUser(username) 
            result = {'username': user.name} 
            if age and age > 10: 
                result['age'] = age 
            return result 
        userinfo.signature = [['struct', 'string'], 
                              ['struct', 'string', 'int']]


Since XML-RPC methods can take different sets of data, each set of valid arguments is its own list. The first value in the list is the type of the return argument. The rest of the arguments are the types of the data that must be passed in. 

In the last method in the example above, since the method can optionally take an integer value, both sets of valid parameter lists should be provided. 

Valid types that can be checked in the signature and their corresponding Python types: 

+--------------------+--------------------+
| XMLRPC             | Python             |
+====================+====================+
| string             | str                |
+--------------------+--------------------+
| array              | list               |
+--------------------+--------------------+
| boolean            | bool               |
+--------------------+--------------------+
| int                | int                |
+--------------------+--------------------+
| double             | float              |
+--------------------+--------------------+
| struct             | dict               |
+--------------------+--------------------+
| dateTime.iso8601   | xmlrpclib.DateTime |
+--------------------+--------------------+
| base64             | xmlrpclib.Binary   |
+--------------------+--------------------+

Note, requiring a signature is optional. 

Also note that a convenient fault handler function is provided. 

.. code-block:: python 

    def xmlrpc_fault(code, message): 
        """Convenience method to return a Pylons response XMLRPC Fault""" 

(The `XML-RPC Home page <http://www.xmlrpc.com/>`_ and the `XML-RPC HOW-TO <http://www.faqs.org/docs/Linux-HOWTO/XML-RPC-HOWTO.html>`_ both provide further detail on the XML-RPC specification.) 

A simple XML-RPC service  
------------------------

This simple service ``test.battingOrder`` accepts a positive integer < 51 as the parameter ``posn`` and returns a string containing the name of the US state occupying that ranking in the order of ratifying the constitution / joining the union. 

.. code-block:: python
 
    import xmlrpclib

    from pylons import request
    from pylons.controllers import XMLRPCController

    states = ['Delaware', 'Pennsylvania', 'New Jersey', 'Georgia',
              'Connecticut', 'Massachusetts', 'Maryland', 'South Carolina',
              'New Hampshire', 'Virginia', 'New York', 'North Carolina',
              'Rhode Island', 'Vermont', 'Kentucky', 'Tennessee', 'Ohio',
              'Louisiana', 'Indiana', 'Mississippi', 'Illinois', 'Alabama',
              'Maine', 'Missouri', 'Arkansas', 'Michigan', 'Florida', 'Texas',
              'Iowa', 'Wisconsin', 'California', 'Minnesota', 'Oregon',
              'Kansas', 'West Virginia', 'Nevada', 'Nebraska', 'Colorado',
              'North Dakota', 'South Dakota', 'Montana', 'Washington', 'Idaho',
              'Wyoming', 'Utah', 'Oklahoma', 'New Mexico', 'Arizona', 'Alaska',
              'Hawaii'] 

    class RpctestController(XMLRPCController): 

        def test_battingOrder(self, posn): 
            """This docstring becomes the content of the 
            returned value for system.methodHelp called with 
            the parameter "test.battingOrder"). The method 
            signature will be appended below ... 
            """ 
            # XML-RPC checks agreement for arity and parameter datatype, so 
            # by the time we get called, we know we have an int. 
            if posn > 0 and posn < 51: 
                return states[posn-1] 
            else: 
                # Technically, the param value is correct: it is an int. 
                # Raising an error is inappropriate, so instead we 
                # return a facetious message as a string. 
                return 'Out of cheese error.' 
        test_battingOrder.signature = [['string', 'int']] 


Testing the service
-------------------

For developers using OS X, there's an `XML/RPC client <http://www.ditchnet.org/xmlrpc/>`_ that is an extremely useful diagnostic tool when developing XML-RPC (it's free ... but not entirely bug-free). Or, you can just use the Python interpreter: 

.. code-block:: pycon

    >>> from pprint import pprint 
    >>> import xmlrpclib 
    >>> srvr = xmlrpclib.Server("http://example.com/rpctest/") 
    >>> pprint(srvr.system.listMethods()) 
    ['system.listMethods', 
     'system.methodHelp', 
     'system.methodSignature', 
     'test.battingOrder'] 
    >>> print srvr.system.methodHelp('test.battingOrder') 
    This docstring becomes the content of the 
    returned value for system.methodHelp called with 
    the parameter "test.battingOrder"). The method 
    signature will be appended below ... 

    Method signature: [['string', 'int']] 
    >>> pprint(srvr.system.methodSignature('test.battingOrder')) 
    [['string', 'int']] 
    >>> pprint(srvr.test.battingOrder(12)) 
    'North Carolina' 

To debug XML-RPC servers from Python, create the client object using the optional verbose=1 parameter. You can then use the client as normal and watch as the XML-RPC request and response is displayed in the console. 

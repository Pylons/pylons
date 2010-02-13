.. _testing:

===========================
Unit and functional testing
===========================

Unit Testing with :mod:`webtest`
================================

Pylons provides powerful unit testing capabilities for your web application 
utilizing `webtest <http://pythonpaste.org/webtest/>`_ 
to emulate requests to your web application. You can then ensure that the 
response was handled appropriately and that the controller set things up 
properly. 

To run the test suite for your web application, Pylons utilizes the `nose 
<http://somethingaboutorange.com/mrl/projects/nose/>`_ test runner/discovery 
package. Running ``nosetests`` in your project directory will run all the 
tests you create in the tests directory. If you don't have nose installed on 
your system, it can be installed via setuptools with: 

.. code-block:: bash 

    $ easy_install -U nose 

To avoid conflicts with your development setup, the tests use the `test.ini` configuration file when run. This means **you must configure any databases, etc. in your test.ini file or your tests will not be able to find the database configuration**. 

.. warning:: 

    Nose can trigger errors during its attempt to search for doc tests since it will try and import all your modules one at a time *before* your app was loaded. This will cause files under models/ that rely on your app to be running, to fail. 

Pylons 0.9.6.1 and later includes a plugin for nose that loads the app before 
the doctests scan your modules, allowing models to be doctested. You can use 
this option from the command line with nose: 

.. code-block:: bash 

    nosetests --with-pylons=test.ini 

Or by setting up a `[nosetests]` block in your setup.cfg: 

.. code-block:: ini 

    [nosetests] 
    verbose=True 
    verbosity=2 
    with-pylons=test.ini 
    detailed-errors=1 
    with-doctest=True 

Then just run: 

.. code-block:: bash 

    python setup.py nosetests 

to run the tests. 

Example: Testing a Controller 
============================= 

First let's create a new project and controller for this example: 

.. code-block:: bash 

    $ paster create -t pylons TestExample 
    $ cd TestExample 
    $ paster controller comments 

You'll see that it creates two files when you create a controller. The stub controller, and a test for it under ``testexample/tests/functional/``. 

Modify the ``testexample/controllers/comments.py`` file so it looks like this: 

.. code-block:: python 

    from testexample.lib.base import * 

    class CommentsController(BaseController): 

        def index(self): 
            return 'Basic output' 

        def sess(self): 
            session['name'] = 'Joe Smith' 
            session.save() 
            return 'Saved a session' 

Then write a basic set of tests to ensure that the controller actions are functioning properly, modify ``testexample/tests/functional/test_comments.py`` to match the following: 

.. code-block:: python 

    from testexample.tests import * 

    class TestCommentsController(TestController): 
        def test_index(self): 
            response = self.app.get(url(controller='/comments')) 
            assert 'Basic output' in response 

        def test_sess(self): 
            response = self.app.get(url(controller='/comments', action='sess')) 
            assert response.session['name'] == 'Joe Smith' 
            assert 'Saved a session' in response 

Run ``nosetests`` in your main project directory and you should see them all pass: 

.. code-block:: pycon 

    .. 
    ---------------------------------------------------------------------- 
    Ran 2 tests in 2.999s 

    OK 

Unfortunately, a plain assert does not provide detailed information about the results of an assertion should it fail, unless you specify it a second argument. For example, add the following test to the ``test_sess`` function: 

.. code-block:: python 

    assert response.session.has_key('address') == True 

When you run ``nosetests`` you will get the following, not-very-helpful result:

.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    assert response.session.has_key('address') == True 
    AssertionError: 


    ---------------------------------------------------------------------- 
    Ran 2 tests in 1.417s 

    FAILED (failures=1) 

You can augment this result by doing the following: 

.. code-block:: python 

    assert response.session.has_key('address') == True, "address not found in session" 

Which results in: 

.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    assert response.session.has_key('address') == True 
    AssertionError: address not found in session 


    ---------------------------------------------------------------------- 
    Ran 2 tests in 1.417s 

    FAILED (failures=1) 

But detailing every assert statement could be time consuming. Our TestController subclasses the standard Python ``unittest.TestCase`` class, so we can use utilize its helper methods, such as ``assertEqual``, that can automatically provide a more detailed AssertionError. The new test line looks like this: 

.. code-block:: python 

    self.assertEqual(response.session.has_key('address'), True) 

Which provides the more useful failure message: 

.. code-block:: pycon 

    .F 
    ====================================================================== 
    FAIL: test_sess (testexample.tests.functional.test_comments.TestCommentsController) 
    ---------------------------------------------------------------------- 
    Traceback (most recent call last): 
    File "~/TestExample/testexample/tests/functional/test_comments.py", line 12, in test_sess 
    self.assertEqual(response.session.has_key('address'), True) 
    AssertionError: False != True 


Testing Pylons Objects 
====================== 

Pylons will provide several additional attributes for the :mod:`webtest` :class:`webtest.TestResponse` object that let you access various objects that were created during the web request: 

``config``
    The configured Pylons applications.
``session`` 
    Session object 
``req`` 
    Request object 
``tmpl_context`` 
    Object containing variables passed to templates 
``app_globals`` 
    Globals object 

To use them, merely access the attributes of the response *after* you've used 
a get/post command: 

.. code-block:: python 

    response = app.get('/some/url') 
    assert response.session['var'] == 4 
    assert 'REQUEST_METHOD' in response.req.environ 

.. note:: 

    The :class:`response <webtest.TestResponse>` object already has a
    TestRequest object assigned to it, therefore Pylons assigns its
    ``request`` object to the response as ``req``. 


Accessing Special Globals
-------------------------

Sometimes, you might wish to modify or check a global Pylons variable such as :term:`app_globals` before running the rest of your unit tests. The non-request specific variables are available from a special URL that will respond only in unit testing situations.

For example, to get the :term:`app_globals` object without sending a request to your actual applications::
    
    response = app.get('/_test_vars')
    app_globals = response.app_globals

Testing Your Own Objects 
======================== 

WebTest's fixture testing allows you to designate your own objects that you'd 
like to access in your tests. This powerful functionality makes it easy to 
test the value of objects that are normally only retained for the duration of 
a single request. 

Before making objects available for testing, its useful to know when your 
application is being tested. WebTest will provide an environ variable called 
``paste.testing`` that you can test for the presence and truth of so that your 
application only populates the testing objects when it has to. 

Populating the :mod:`webtest` response object with your objects is done by 
adding them to the environ dict under the key ``paste.testing_variables``. 
Pylons creates this dict before calling your application, so testing for its 
existence and adding new values to it is recommended. All variables assigned 
to the ``paste.testing_variables`` dict will be available on the response 
object with the key being the attribute name. 

.. note::

    WebTest is an extracted stand-alone version of a Paste component called
    paste.fixture. For backwards compatibility, WebTest continues to honor
    the ``paste.testing_variables`` key in the environ.

Example: 

.. code-block:: python 

    # testexample/lib/base.py 

    from pylons import request
    from pylons.controllers import WSGIController
    from pylons.templating import render_mako as render

    class BaseController(WSGIController): 
        def __call__(self, environ, start_response): 
            # Create a custom email object 
            email = MyCustomEmailObj() 
            email.name = 'Fred Smith' 
            if 'paste.testing_variables' in request.environ: 
                request.environ['paste.testing_variables']['email'] = email 
            return WSGIController.__call__(self, environ, start_response) 


    # testexample/tests/functional/test_controller.py 
    from testexample.tests import * 

    class TestCommentsController(TestController): 
        def test_index(self): 
            response = self.app.get(url(controller='/')) 
            assert response.email.name == 'Fred Smith' 


.. seealso::

    `WebTest Documentation <http://pythonpaste.org/webtest/>`_
        Documentation covering webtest and its usage
    
    :mod:`WebTest Module docs <webtest>`
        Module API reference for methods available for use when testing
        the application

.. _unit_testing:

Unit Testing
============

XXX: Describe unit testing an applications models, libraries


.. _functional_testing:

Functional Testing
==================

XXX: Describe functional/integrated testing, WebTest

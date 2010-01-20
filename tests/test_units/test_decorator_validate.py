# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

from pylons.decorators import validate

from pylons.controllers import WSGIController

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

import formencode
from formencode.htmlfill import html_quote

def custom_error_formatter(error):
    return '<p><span class="pylons-error">%s</span></p>\n' % html_quote(error)

class NetworkForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    new_network = formencode.validators.URL(not_empty=True)

class HelloForm(formencode.Schema):
    hello = formencode.ForEach(formencode.validators.Int())

class ValidatingController(WSGIController):
    def new_network(self):
        return """
<html>
  <form action="/dhcp/new_form" method="POST">
    <table>
      <tr>
        <th>Network</th>
        <td>
          <input id="new_network" name="new_network" type="text" value="" />
        </td>
      </tr>
    </table>
    <input name="commit" type="submit" value="Save changes" />
  </form>
</html>
"""

    @validate(schema=NetworkForm, form='new_network')
    def network(self):
        return 'Your network is: %s' % self.form_result.get('new_network')

    def view_hello(self):
        return """
<html>
  <form action="/hello" method="POST">
    <table>
      <tr>
        <th>Hello</th>
        <td>
          <form:iferror name="hello">Bad Hello!&nbsp;</form:iferror>
          <input id="hello" name="hello" type="text" value="" />
          <input id="hello" name="hello" type="text" value="" />
          <input id="hello" name="hello" type="text" value="" />
        </td>
      </tr>
    </table>
    <input name="commit" type="submit" value="Submit" />
  </form>
</html>
"""

    @validate(schema=HelloForm(), post_only=False, form='view_hello')
    def hello(self):
        return str(self.form_result)

    @validate(schema=HelloForm(), post_only=False, form='view_hello',
              auto_error_formatter=custom_error_formatter)
    def hello_custom(self):
        return str(self.form_result)

    @validate(schema=NetworkForm, form='hello_recurse')
    def hello_recurse(self, environ):
        if environ['REQUEST_METHOD'] == 'GET':
            return self.new_network()
        else:
            return 'Your network is: %s' % self.form_result.get('new_network')


class TestValidateDecorator(TestWSGIController):
    def setUp(self):
        TestWSGIController.setUp(self)
        app = SetupCacheGlobal(ControllerWrap(ValidatingController),
                               self.environ)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_network_validated(self):
        response = self.post_response(action='network',
                                      new_network='http://pylonshq.com/')
        assert 'Your network is: http://pylonshq.com/' in response

    def test_network_failed_validation_non_ascii(self):
        response = self.post_response(action='network', new_network='Росси́я')
        assert 'That is not a valid URL' in response
        assert 'Росси́я' in response

    def test_recurse_validated(self):
        response = self.post_response(action='hello_recurse',
                                      new_network='http://pylonshq.com/')
        assert 'Your network is: http://pylonshq.com/' in response

    def test_hello(self):
        self.environ['pylons.routes_dict']['action'] = 'hello'
        response = self.app.post('/hello?hello=1&hello=2&hello=3',
                                 extra_environ=self.environ)
        assert "{'hello': [1, 2, 3]}" in response
                                      
    def test_hello_failed(self):
        self.environ['pylons.routes_dict']['action'] = 'hello'
        response = self.app.post('/hello?hello=1&hello=2&hello=hi',
                                 extra_environ=self.environ)
        assert 'Bad Hello!&nbsp;' in response
        assert "[None, None, u'Please enter an integer value']" in response

    def test_hello_custom_failed(self):
        self.environ['pylons.routes_dict']['action'] = 'hello_custom'
        response = \
            self.app.post('/hello_custom?hello=1&hello=2&hello=hi',
                          extra_environ=self.environ)
        assert 'Bad Hello!&nbsp;' in response
        assert "[None, None, u'Please enter an integer value']" in response
        assert ("""<p><span class="pylons-error">[None, None, u'Please enter """
                """an integer value']</span></p>""") in response

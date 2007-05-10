# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

from pylons import Response
from pylons.decorators import validate

from pylons.controllers import WSGIController

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

import formencode

class NetworkForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    new_network = formencode.validators.URL(not_empty=True)

class ValidatingController(WSGIController):
    def new(self):
        return Response("""
<html>
  <form action="/dhcp/new_form" method="POST">
    <table>
      <tr>
        <th>Network</th>
        <td>
          <input id="new_network" name="new_network" type="text" class="error" value="" />
        </td>
      </tr>
    </table>
    <input name="commit" type="submit" value="Save changes" />
  </form>
</html>
                        """)

    def network(self):
        return Response('Your network is: %s' %
            self.form_result.get('new_network'))
    network = validate(schema=NetworkForm, form='new')(network)

class TestValidateDecorator(TestWSGIController):
    def setUp(self):
        TestWSGIController.setUp(self)
        app = SetupCacheGlobal(ControllerWrap(ValidatingController),
                               self.environ, setup_cache=False)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_validated(self):
        response = self.post_response(action='network',
                                      new_network='http://pylonshq.com/')
        assert 'Your network is: http://pylonshq.com/' in response

    def test_failed_validation_non_ascii(self):
        response = self.post_response(action='network', new_network='Росси́я')
        print response
        assert 'That is not a valid URL' in response
        assert 'Росси́я' in response

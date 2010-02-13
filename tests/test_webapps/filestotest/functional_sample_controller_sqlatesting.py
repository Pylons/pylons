from projectname.tests import *
from sqlalchemy.exceptions import IntegrityError
from projectname.model.meta import Session, Base
from projectname.model import Foo

class TestSQLAlchemyController(TestController):
    def setUp(self):
        Base.metadata.create_all(bind=Session.bind)
        f = Foo(id = 1, bar = u"Wabbit")
        Session.add(f)
        Session.commit()
        assert f.bar == u"Wabbit"
    
    def tearDown(self):
        Base.metadata.drop_all(bind=Session.bind)

    def test_sqlalchemy(self):
        response = self.app.get(url(controller='sample', action='testsqlalchemy'))
        assert 'foos = [Foo:1]' in response

    # def test_exception(self):
    #     me = Foo(id=3, bar='giuseppe')
    #     me_again = Foo(id=3, bar='giuseppe')
    #     self.assertRaises(IntegrityError, Session.commit)
    #     Session.rollback()

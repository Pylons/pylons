"""The application's model objects"""
from sqlalchemy import types, Column

from projectname.model.meta import Base, Session

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)


class Foo(Base):
    __tablename__ = 'foo'

    id = Column(types.Integer, primary_key=True)
    bar = Column(types.String(255), nullable=False)
    def __repr__(self):
        return "Foo:%s" % self.id

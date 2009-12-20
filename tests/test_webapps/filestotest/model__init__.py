"""The application's model objects"""
from projectname.model.meta import Session, metadata

from sqlalchemy import types, Column
from sqlalchemy.ext.declarative import declarative_base

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = Table("Reflected", metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    Session.configure(bind=engine)

## Declarative object definitions
## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html
#
Base = declarative_base(metadata=metadata)

class Foo(Base):
    __tablename__ = 'foo'

    id = Column(types.Integer, primary_key=True)
    bar = Column(types.String(255), nullable=False)
    def __repr__(self):
        return "Foo:%s" % self.id

## Non-reflected tables
## http://www.sqlalchemy.org/docs/05/ormtutorial.html
#
#foo_table = metadata,
#    Column("id", types.Integer, primary_key=True),
#    Column("bar", types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Reflected tables
## Note: The table and mapping itself must be done in the init_model function
#
#reflected_table = None
#
#class Reflected(object):
#    pass

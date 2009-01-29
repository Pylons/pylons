"""The application's model objects"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

from tmpapp.model import meta

_Base = declarative.declarative_base()

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    #### REFLECTED TABLES must be defined and mapped here!!!
    # (Their ORM classes may be defined at the global level.)
    #
    #global reflected_table
    #reflected_table = sa.Table("reflected", meta.metadata, autoload=True,
    #    autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    
    sm = orm.sessionmaker(bind=engine)

    meta.Session = orm.scoped_session(sm)
    meta.engine = engine


#### NON-REFLECTED tables may be defined and mapped here.

class Simple(_Base):
    __tablename__ = "simple"
    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.String(100))

#### Using the Declarative extension.
#
# class Person(_Base):
#     __tablename__ = "persons"
#     id = sa.Column(sa.types.Integer, primary_key=True)


#### Not using the Declarative extension.
#
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


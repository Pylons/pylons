import sqlalchemy as sa
import tmpapp.model as model
import tmpapp.model.meta as meta

DB_URL = "sqlite:///test.sqlite"

engine = sa.create_engine(DB_URL)
model.init_model(engine)

model._Base.metadata.drop_all(bind=meta.engine, checkfirst=True)
model._Base.metadata.create_all(bind=meta.engine)

a = model.Simple()
a.name = "Aaa"
meta.Session.save(a)

b = model.Simple()
b.name = "Bbb"
meta.Session.save(b)

meta.Session.commit()



print "Database data:"
for simp in meta.Session.query(model.Simple):
    print "id:", simp.id
    print "name:", simp.name
    print


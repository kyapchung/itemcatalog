#!usr/bin/env python2.7
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Catalog Categories and starter items
category1 = Category(id=1, name="Muppets")

session.add(category1)
session.commit()

Item1 = Item(id=1, name="Grover", description="He's blue and stuff!",
             creator='1', category=category1)

session.add(Item1)
session.commit()

category2 = Category(id=2, name="Musical Instruments")

session.add(category2)
session.commit()

Item2 = Item(id=2, name="Banjo", description="For that country twang!",
             creator='1', category=category2)

session.add(Item2)
session.commit()

Item3 = Item(id=3, name="Guitar", description="Strum a little diddy!",
             creator='1', category=category2)

session.add(Item3)
session.commit()

category3 = Category(id=3, name="Boats")

session.add(category3)
session.commit()

category4 = Category(id=4, name="Candy")

session.add(category4)
session.commit()

category5 = Category(id=5, name="Countries")

session.add(category5)
session.commit()

print "Added starter catagories and items!"

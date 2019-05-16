#!usr/bin/env python2.7
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    '''Registered User information is stored in the DB'''
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }


class Category(Base):
    '''Stores predefined item categories in the database'''
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    '''Stores item information in the DB'''
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    creator = Column(Integer, nullable=False)
    category_name = Column(String, ForeignKey('category.name'))
    category = relationship(Category, cascade="save-update, delete")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'creator': self.creator,
            'description': self.description,
            'category_name': self.category_name,
        }


engine = create_engine('postgresql://itemcatalog:udacity@localhost/itemcatalog')

Base.metadata.create_all(engine)

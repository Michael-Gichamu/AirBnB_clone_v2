#!/usr/bin/python3
"""Database storage engine"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}

class DBStorage:
    """
    Database storage engine for mysql storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate new dbstorage instance"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                                           HBNB_MYSQL_USER,
                                           HBNB_MYSQL_PWD,
                                           HBNB_MYSQL_HOST,
                                           HBNB_MYSQL_DB
                                        ), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current db session all cls objects"""
        new_dict = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Adds the obj to the current db session"""
        if obj is not None:
                self.__session.add(obj)
                self.__session.flush()
    def save(self):
        """Commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes objects from current database session and does nothing if
        obj is None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close session"""
        self.__session.close()

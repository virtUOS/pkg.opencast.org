# -*- coding: utf-8 -*-
'''
Database specification for the Opencast package repository user interface.
:license: FreeBSD, see license file for more details.
'''

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


def init():
    '''Initialize connection to database and create database structure if
    non-existent.
    '''
    global engine
    engine = create_engine(config.database)
    Base.metadata.create_all(engine)


def get_session():
    '''Get a session for database communication. If necessary a new connection
    to the database will be established.

    :return:  Database session
    '''
    if 'engine' not in globals():
        init()
    Session = sessionmaker(bind=engine)
    return Session()


# Database Schema Definition
class User(Base):
    '''Database definition for users.'''

    __tablename__ = 'user'

    username = Column('username', String(length=255), primary_key=True)
    '''Unique username'''
    access = Column('access', Boolean(), nullable=False)
    admin = Column('admin', Boolean(), nullable=False)
    city = Column('city', Text(), nullable=False)
    comment = Column('comment', Text(), nullable=True)
    country = Column('country', Text(), nullable=False)
    created = Column('created', DateTime(), nullable=False)
    department = Column('department', Text(), nullable=True)
    email = Column('email', Text(), nullable=False)
    firstname = Column('firstname', Text(), nullable=False)
    lastname = Column('lastname', Text(), nullable=False)
    learned = Column('learned', Text(), nullable=True)
    organization = Column('organization', Text(), nullable=False)
    password = Column('password', Text(), nullable=True)
    salt = Column('salt', Text(), nullable=True)
    usage = Column('usage', Text(), nullable=True)

    def __repr__(self):
        '''Return a string representation of an user object.

        :return: String representation of object.
        '''
        return '<User=%s, firstname="%s", lastname="%s")>' % \
               (self.username, self.firstname, self.lastname)

    def serialize(self, expand=0):
        '''Serialize this object as dictionary usable for conversion to JSON.

        :param expand: Defines if sub objects shall be serialized as well.
        :return: Dictionary representing this object.
        '''
        return {
            'username': self.username,
            'access': self.access,
            'admin': self.admin,
            'city': self.city,
            'comment': self.comment,
            'country': self.country,
            'created': self.created,
            'department': self.department,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'learned': self.learned,
            'organization': self.organization,
            'password': self.password,
            'salt': self.salt,
            'usage': self.usage
            }

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
from passlib.hash import pbkdf2_sha512
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime, Boolean, create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship, backref
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
    country = Column('country', Text(), nullable=False)
    created = Column('created', DateTime(), nullable=False)
    department = Column('department', Text(), nullable=True)
    email = Column('email', Text(), nullable=False, unique=True)
    firstname = Column('firstname', Text(), nullable=False)
    lastname = Column('lastname', Text(), nullable=False)
    learned = Column('learned', Text(), nullable=True)
    organization = Column('organization', Text(), nullable=False)
    password = Column('password', Text(), nullable=True)
    usage = Column('usage', Text(), nullable=True)

    def password_set(self, password):
        self.password = pbkdf2_sha512.encrypt(password)

    def password_verify(self, password):
        return pbkdf2_sha512.verify(password, self.password)

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


class ActivationLink(Base):
    '''Database definition for users.'''

    __tablename__ = 'activationlink'

    username = Column('username', ForeignKey('user.username'), primary_key=True)
    '''Unique username'''
    key = Column('key', Text(), nullable=False)
    created = Column('created', DateTime(), nullable=False)

    user = relationship('User', backref=backref('activationlink'))
    '''User related to this activation link'''

    def __repr__(self):
        '''Return a string representation of an user object.

        :return: String representation of object.
        '''
        return '<User=%s, key="%s", created="%s")>' % \
               (self.username, self.key, self.created)

    def serialize(self, expand=0):
        '''Serialize this object as dictionary usable for conversion to JSON.

        :param expand: Defines if sub objects shall be serialized as well.
        :return: Dictionary representing this object.
        '''
        return {
            'username': self.username,
            'key': self.key,
            'created': self.created
            }

from sqlalchemy import Table, Column, Integer, String, Binary, Boolean
from sqlalchemy.orm import mapper

from database import metadata, db_session


class User():
    query = db_session.query_property()

    def __init__(self, username, password, salt, email, first_name,
                 last_name):
        self.username = username
        self.password = password
        self.salt = salt
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User %r>' % (self.username)


users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(255)),
              Column('password', Binary(64)),
              Column('salt', String(42)),
              Column('token', String(32)),
              Column('email', String(255)),
              Column('first_name', String(255)),
              Column('last_name', String(255)),
              Column('Premium', Boolean, default=False),
              )

mapper(User, users)

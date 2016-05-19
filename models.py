from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Binary, Boolean, DateTime
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
        self.created_date = datetime.now

    def __repr__(self):
        return '<User %r>' % (self.username)

    def from_token(token):
        if token:
            return User.query.filter(
                User.token == token).first()

    def as_private_dict(self):
        priv_dict = {
            'id': self.id,
            'username': self.username.decode('utf-8'),
            'first_name': self.first_name.decode('utf-8'),
            'last_name': self.last_name.decode('utf-8'),
            'email': self.email.decode('utf-8'),
            'created_at': self.created_at
            }
        return priv_dict


users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(255)),
              Column('password', Binary(64)),
              Column('salt', String(42)),
              Column('token', String(32)),
              Column('email', String(255)),
              Column('first_name', String(255)),
              Column('last_name', String(255)),
              Column('created_at', DateTime, default=datetime.now),
              Column('Premium', Boolean, default=False),
              )

mapper(User, users)

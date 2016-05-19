import os
import sys
import random
import string
import hashlib
import uuid
import binascii

from flask import Flask, request, jsonify, redirect, session
from database import db_session, init_db, init_engine

import wrappers
from models import User


app = Flask(__name__)


def get_hash(password, salt):
    m = hashlib.sha512()
    m.update(salt)
    m.update(password)
    return m.digest()


def check_token(token):
    return User.query.filter(User.token == token).first() == token


def new_user(username, password, email, first_name, last_name):
    salt = os.urandom(32)
    hashpass = get_hash(password, salt)

    if not User.query.filter(User.username == username).first() and not \
       User.query.filter(User.email == email).first():
        user = User(username, hashpass, salt, email, first_name, last_name)
        db_session.add(user)
        db_session.commit()
    else:
        return -1

    return user


@app.route('/user', methods=['POST'])
def create_user():
    req = request.get_json(force=True)
    if 'username' not in req or 'password' not in req or 'email' not in req \
            or 'first_name' not in req or 'last_name' not in req:
        return jsonify({'error': 'Bad request'}), 400
    username = req['username'].encode("utf8")
    password = req['password'].encode("utf8")
    email = req['email'].encode("utf8")
    first_name = req['first_name'].encode("utf8")
    last_name = req['last_name'].encode("utf8")

    if new_user(username, password, email, first_name, last_name) == -1:
        return jsonify({'message': 'username or email already exists.'}), 409
    else:
        return jsonify({'message': 'user created.'}), 200


@app.route('/login', methods=['GET'])
def get_login():
    pass


@app.route('/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    if 'username' not in req or 'password' not in req:
        return jsonify({'error': 'Bad request'}), 400
    username = req['username'].encode("utf8")
    password = req['password'].encode("utf8")

    user = User.query.filter(User.username == username).first()
    if user and get_hash(password, user.salt) == user.password:
        token = uuid.uuid4().hex
        user.token = token

        db_session.query(User).filter_by(id=user.id) \
            .update({"token": user.token})
        db_session.commit()

        resp = jsonify({'message': "login successful", 'token': token})
        return resp

    return jsonify({'message': 'Bad login'}), 401


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config.from_pyfile('config/config.py')

    if len(sys.argv) == 2:
        conf = sys.argv[1]
        print('Loading additional config %s...', conf)
        app.config.from_pyfile('config/' + conf + '_config.py')

    init_engine(app.config['DATABASE_URI'])
    init_db()
    app.run(host='0.0.0.0')

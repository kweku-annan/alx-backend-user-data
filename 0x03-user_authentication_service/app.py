#!/usr/bin/env python3
"""Basic Flask app"""

from flask.helpers import make_response
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home():
    """Home function"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Implements the end-point /users"""
    data = request.form
    email, password = data.get('email'), data.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Implements the login function"""
    data = request.form
    email, password = data.get('email'), data.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    response = make_response(jsonify(
        {"email": email, "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(email))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

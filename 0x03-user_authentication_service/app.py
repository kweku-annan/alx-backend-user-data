#!/usr/bin/env python3
"""Basic Flask app"""
from crypt import methods

from flask.helpers import make_response
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """End session for user"""
    user_cookie = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Implements profile function"""
    user_cookie = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

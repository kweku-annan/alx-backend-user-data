#!/usr/bin/env python3
"""Model for auth"""
import uuid

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User
from typing import Union


def _hash_password(password: str) -> bytes:
    """Takes a password, hashes it and returns a byte"""

    # Convert password to byte
    password = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register's User following authentication protocol"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Returns the session_id of a user"""
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id) -> Union[User, None]:
        """Get's user by session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id) -> None:
        """Updates corresponding user_id's session to None"""
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except ValueError:
            pass
        return None

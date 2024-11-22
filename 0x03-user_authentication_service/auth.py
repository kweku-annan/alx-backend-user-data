#!/usr/bin/env python3
"""Model for auth"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Takes a password, hashes it and returns a byte"""

    # Convert password to byte
    password = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd


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
            user = self._db.add_user(email, str(hashed_pwd))
            return user

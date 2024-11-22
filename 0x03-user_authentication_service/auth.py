#!/usr/bin/env python3
"""Model for auth"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes a password, hashes it and returns a byte"""

    # Convert password to byte
    password = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd

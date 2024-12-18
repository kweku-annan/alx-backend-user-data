#!/usr/bin/env python3
"""Implements Basic authentication class"""
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Performs the function of a basic authication"""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip("Basic ")

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of Base64 string base64_authorization"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base64_authorization_header
            return base64.b64decode(decoded, validate=True).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not type(decoded_base64_authorization_header) is str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Returns the User instance based on email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves User interface for a request"""
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        b64_auth_header_decode = self.decode_base64_authorization_header(
            b64_auth_header
        )
        email, password = self.extract_user_credentials(b64_auth_header_decode)
        user_instance = self.user_object_from_credentials(email, password)
        return user_instance

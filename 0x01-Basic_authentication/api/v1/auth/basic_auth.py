#!/usr/bin/env python3
"""Implements Basic authentication class"""
from api.v1.auth.auth import Auth


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

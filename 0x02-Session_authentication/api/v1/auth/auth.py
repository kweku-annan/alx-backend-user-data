#!/usr/bin/env python3
"""Manages the API authentication"""
from typing import List, TypeVar

from flask import request


class Auth:
    """A class to manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False"""

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path not in excluded_paths and f"{path}/" not in excluded_paths:
            return True

        if path in excluded_paths or f"{path}/" in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from request"""
        from os import getenv
        if request is None:
            return None
        my_session_name = getenv("SESSION_NAME", "_my_session_id")
        cookie = request.cookies.get(my_session_name)
        return cookie

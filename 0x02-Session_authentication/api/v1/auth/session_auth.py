#!/usr/bin/env python3
"""Implements the Session Authentication of this program"""
from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """Class for Session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a instance based on cookie value"""
        session_cookie = self.session_cookie(request)

        if session_cookie is None:
            return None
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

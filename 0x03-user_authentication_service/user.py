#!/usr/bin/env python3
"""SQLAlchemy Model for User Database"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String


Base = declarative_base()


class User(Base):
    """Defines or maps the users database"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

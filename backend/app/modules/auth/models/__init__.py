"""Barrel module separado por entidades do banco"""
from .refresh_token import RefreshToken
from .user import User

__all__ = ["User", "RefreshToken"]
#!/usr/bin/env python3
"""
Custom authentication helpers for messaging app.
"""

from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_for_user(user):
    """
    Generate access + refresh tokens for a user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

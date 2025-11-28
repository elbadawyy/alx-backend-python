#!/usr/bin/env python3
"""
Custom permissions for conversations and messages.
"""

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the conversation. Applies to GET, POST, PUT, PATCH, DELETE.
    """

    allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        # Must be authenticated
        if not (request.user and request.user.is_authenticated):
            return False

        # Ensure method is allowed to be checked
        if request.method not in self.allowed_methods:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - sender or receiver (message)
        - OR user is in conversation participants
        """
        user = request.user

        return (
            getattr(obj, "sender", None) == user or
            getattr(obj, "receiver", None) == user or
            user in getattr(obj, "participants", [])
        )

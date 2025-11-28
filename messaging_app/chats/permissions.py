#!/usr/bin/env python3
"""
Custom permissions for messaging app.
"""

from rest_framework import permissions


class IsOwnerOfMessage(permissions.BasePermission):
    """
    Allow users to access ONLY their own messages and conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

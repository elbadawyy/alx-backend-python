#!/usr/bin/env python3
"""
Custom permissions for messaging app.
"""

from rest_framework.permissions import BasePermission


class IsOwnerOfMessage(BasePermission):
    """
    Allow users to access ONLY their own messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

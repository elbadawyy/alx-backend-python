#!/usr/bin/env python3
"""
Custom permissions for conversations and messages.
"""

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the conversation.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj must have sender and receiver attributes
        return (
            obj.sender == request.user or
            obj.receiver == request.user or
            request.user in getattr(obj, "participants", [])
        )

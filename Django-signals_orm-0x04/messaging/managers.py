#!/usr/bin/env python3
"""
Custom model managers for messaging app.
"""
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Manager that returns unread messages for a given user.
    """

    def unread_for_user(self, user):
        """
        Return a queryset of unread Message instances for the provided user.
        """
        return self.get_queryset().filter(receiver=user, read=False)

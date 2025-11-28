from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )

    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_messages"
    )
    
    read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"

# Model to store old versions of messages
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
    
    
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # returns unread messages for the given user
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "created_at")
        )


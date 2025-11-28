#!/usr/bin/env python3
from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return self.title


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

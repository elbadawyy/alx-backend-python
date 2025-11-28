#!/usr/bin/env python3
from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth.models import User

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'participants']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at']
        read_only_fields = ['conversation', 'sender', 'created_at']


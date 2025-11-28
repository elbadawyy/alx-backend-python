#!/usr/bin/env python3
"""
Views for messaging app.
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsParticipantOfConversation
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied(detail="You are not a participant of this conversation.")

        return Message.objects.filter(conversation=conversation).order_by('-created_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if not conversation.participants.filter(id=self.request.user.id).exists():
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

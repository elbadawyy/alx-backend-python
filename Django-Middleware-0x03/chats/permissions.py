from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = obj.conversation

        if not conversation.participants.filter(id=request.user.id).exists():
            return False

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == request.user

        return True

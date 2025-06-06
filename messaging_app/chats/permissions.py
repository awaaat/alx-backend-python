from rest_framework import permissions, BasePermission # type: ignore
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Conversation):
            return obj.participants.filter(id = request.user.id).exists()
        return False
        
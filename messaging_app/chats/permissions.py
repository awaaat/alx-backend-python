from rest_framework import permissions, BasePermission # type: ignore
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission class to restrict access to conversations and messages.
    Ensures only authenticated users who are participants in a conversation
    can perform actions (view, send, update, delete).
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated for general API access.
        Applies to all requests (GET, POST, PUT, PATCH, DELETE).
        """
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        - Allows GET, HEAD, OPTIONS (safe methods) for participants to view.
        - Allows PUT, PATCH, DELETE only for participants to update/delete.
        - Supports both Conversation and Message objects.
        """
        # Deny access if user is not authenticated
        if not request.user.is_authenticated:
            return False
        # Allow access if user is not authenticated
        if isinstance(obj, Conversation):
            conversation = obj
        elif  isinstance(obj, Message):
            message = obj
        else:
            return False
        # Check if user is a participant in the conversation
        is_participant = conversation.participants.filter(id = request.user.id).exists()
        # Allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            return is_participant
        # Explicitly allow PUT, PATCH, DELETE for participants only
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant

        # Allow POST for creating messages if user is a participant
        return is_participant
    
    
        
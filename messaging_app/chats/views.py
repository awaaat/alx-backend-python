from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework import serializers
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Allows authenticated users to create, view, and manage conversations they participate in.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['updated_at']
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return conversations where the authenticated user is a participant.
        """
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation and return its details.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages in conversations.
    Allows participants to send, view, update, and delete messages.
    Supports filtering by conversation and search/ordering by message content or sender.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    permission_classes = [IsParticipantOfConversation]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Return messages for a specific conversation or all conversations the user participates in.
        Filters by conversation_id (if provided) and user participation.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new message in the specified conversation.
        Sets the sender as the authenticated user and links to the conversation.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

    def update(self, request, *args, **kwargs):
        """
        Update a message if the user is a participant in the conversation.
        Returns HTTP_403_FORBIDDEN if the user is not authorized.
        """
        instance = self.get_object()
        # Explicitly check if the message belongs to a conversation the user participates in
        if not Message.objects.filter(
            id=instance.id,
            conversation__participants=self.request.user
        ).exists():
            return Response(
                {"detail": "You are not authorized to update this message"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a message if the user is a participant in the conversation.
        Returns HTTP_403_FORBIDDEN if the user is not authorized.
        """
        instance = self.get_object()
        # Explicitly check if the message belongs to a conversation the user participates in
        if not Message.objects.filter(
            id=instance.id,
            conversation__participants=self.request.user
        ).exists():
            return Response(
                {"detail": "You are not authorized to delete this message"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user data.
    Returns ordered user list to support pagination.
    """
    queryset = User.objects.all().order_by('user_id')  # Add ordering to fix pagination warning
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    """
    Retrieve the authenticated user's profile data.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
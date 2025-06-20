from rest_framework import viewsets, filters, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_extensions.cache.decorators import cache_response
from typing import Optional
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import ChatUser, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import CustomPagination
import logging

logger = logging.getLogger(__name__)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants')
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['updated_at']
    permission_classes = [IsParticipantOfConversation]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return self.queryset.filter(participants=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing messages within conversations.
    Supports CRUD operations with nested routing under conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['sender__first_name', 'sender__last_name']
    ordering_fields = ['timestamp']
    permission_classes = [IsParticipantOfConversation]
    filterset_class = MessageFilter
    pagination_class = CustomPagination

    def get_queryset(self) -> QuerySet:
        """
        Customize queryset to filter messages based on conversation_id or user_id.
        """
        conversation_id = self.kwargs.get('conversation_id')
        user_id = self.kwargs.get('user_id')
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id = conversation_id,
                conversation__participants= self.request.user
            ).order_by('-timestamp')[:10]

        if user_id:
            return Message.objects.filter(
                sender__user_id=user_id,
                conversation__participants=self.request.user
            ).order_by('-timestamp')

        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by('-timestamp')

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread(self, request):
        """List unread messages for the authenticated user."""
        messages = Message.unread.unread_for_user(self.request.user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsParticipantOfConversation],
        url_path='conversation/(?P<conversation_id>[^/.]+)'
    )
    @cache_response(60)
    def get_conversation_messages(self, request, conversation_id: Optional[str] = None):
        """List messages in a conversation, cached for 60 seconds."""
        messages = Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).select_related('sender').only(
            'message_id', 'sender__username', 'message_body', 'timestamp'
        ).order_by('timestamp')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create', url_name='message-create')
    def create_message(self, request, conversation_id_pk: Optional[str] = None) -> Response:
        """
        Create a new message in the specified conversation.
        """
        if not conversation_id_pk:
            logger.error("Attempted message creation without conversation_id")
            raise ValidationError({"detail": "Missing conversation_id in URL."})

        try:
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id_pk)
        except ValueError:
            logger.error(f"Invalid conversation_id format: {conversation_id_pk}")
            raise ValidationError({"detail": "Invalid conversation_id format."})

        if request.user not in conversation.participants.all():
            logger.warning(f"User {request.user.user_id} attempted to post to unauthorized conversation {conversation_id_pk}")
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        data= request.data.copy()
        data['conversation'] = conversation_id_pk
        data['sender'] = request.user.user_id
        
        parent_message_id = data.get('parent_message')
        if parent_message_id:
            parent_message = get_object_or_404(Message, message_id = parent_message_id)
            if not Message.objects.filter(
                message_id = parent_message_id,
            conversation__participants = request.user
            ).exists():
                raise ValidationError("Error. You do not have access to this conversation")
            data['parent_message'] = parent_message_id
                

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Infer receiver: the other participant in the conversation
        receiver = conversation.participants.exclude(user_id=request.user.user_id).first()
        if not receiver:
            raise ValidationError("Could not determine receiver — conversation must have 2 participants.")

        
        serializer.save(sender=request.user, receiver=receiver, conversation=conversation)
        logger.info(f"Message created successfully in conversation {conversation_id_pk} by user {request.user.user_id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        """
        Update an existing message with authorization check.
        """
        instance = self.get_object()
        if not Message.objects.filter(
            id=instance.message_id,
            conversation__participants=self.request.user
        ).exists():
            logger.warning(f"Unauthorized update attempt on message {instance.message_id} by user {request.user.user_id}")
            return Response(
                {"detail": "You are not authorized to update this message"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Delete an existing message with authorization check.
        """
        instance = self.get_object()
        if not Message.objects.filter(
            message_id=instance.message_id,
            conversation__participants=self.request.user
        ).exists():
            logger.warning(f"Unauthorized delete attempt on message {instance.message_id} by user {request.user.user_id}")
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
    queryset = ChatUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    """
    Retrieve the authenticated user's profile data.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
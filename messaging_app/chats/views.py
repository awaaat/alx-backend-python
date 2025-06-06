from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework import serializers
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['updated_at']
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    permission_classes = [IsParticipantOfConversation]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return self.queryset.filter(conversation__conversation_id=conversation_id, conversation__participants=self.request.user)
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('user_id')  # Add ordering to fix pagination warning
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
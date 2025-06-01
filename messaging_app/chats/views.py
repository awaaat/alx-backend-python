from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import User, Messages, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    #permission_classes = [IsAuthenticated]
    
    def create_add(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
class MessageViewset(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class  = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'first_name'
    
class MessageDetailsView(generics.RetrieveAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'message_id'
class ConversationDetailsView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'conversation_id'   
from rest_framework import serializers
from .models import User, Conversation, Messages

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
            'bio',
            )

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.CharField(source = 'conversation.conversation_id')
    sender_first_name = serializers.CharField(source = 'sender.first_name')
    sender_last_name = serializers.CharField(source = 'sender.last_name')
    class Meta:
        model = Messages
        fields = (
            'conversation',
            'sender_first_name',
            'sender_last_name',
            'sent_at',
            'message_body',
            'message_id',
            )

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many = True, read_only = True)
    messages = MessageSerializer(many = True, read_only = True)
    class Meta:
        model = Conversation
        fields = (
            #'conversation_id',
            'created_at',
            'updated_at',
            'participants',
            'messages',
        )
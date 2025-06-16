from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
            'bio',
        )

class MessageSerializer(serializers.ModelSerializer):
    sender_first_name = serializers.CharField(source='sender.first_name', read_only = True)
    sender_last_name = serializers.CharField(source='sender.last_name', read_only = True)

    class Meta:
        model = Message
        fields = (
            'message_id',
            'conversation',
            'sender_first_name',
            'sender_last_name',
            'sent_at',
            'message_body',
        )
    
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message Body Cannot Be Empty")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'created_at',
            'updated_at',
            'participants',
            'messages',  
        )

        
from rest_framework import serializers
from .models import User, Conversation, Message

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
            return serializers.ValidationError("Message Body Cannnot Be Empty")
        return value
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many = True, read_only = True)
    message = serializers.SerializerMethodField()
    
    def get_message(self, obj):
        message = Message.objects.filter(conversation = obj)
        return MessageSerializer(message, many = True).data
        
    class Meta:
        model = Conversation
        fields = (
            #'conversation_id',
            'created_at',
            'updated_at',
            'participants',
            'message',
        )
        
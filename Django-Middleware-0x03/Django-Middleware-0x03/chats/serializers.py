from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
            'bio',
        )

class MessageSerializer(serializers.ModelSerializer):
    sender_first_name = serializers.CharField(source='sender.first_name')
    sender_last_name = serializers.CharField(source='sender.last_name')

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
    message_list = serializers.SerializerMethodField()
    def get_message_list(self, obj):  
        """
        Retrieve all messages for the conversation.
        """
        message_list = Message.objects.filter(conversation=obj)
        serializer = MessageSerializer(message_list, many=True)
        return serializer.data

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'created_at',
            'updated_at',
            'participants',
            'message_list',  
        )

        
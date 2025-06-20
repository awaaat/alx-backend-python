from rest_framework import serializers
from .models import ChatUser, Conversation, Message
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ('user_id', 'first_name', 'last_name', 'phone_number')

class MessageSerializer(serializers.ModelSerializer):
    sender_first_name = serializers.CharField(source='sender.first_name', read_only=True)
    #sender_last_name = serializers.CharField(source='sender.last_name', read_only=True)
    #conversation = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_messages = serializers.PrimaryKeyRelatedField(
        queryset = Message.objects.all(),
        allow_null = True,
        required = False,
        help_text="ID of any message this is a reply to (optional, across accessible conversations)"
    )
    class Meta:
        model = Message
        fields = ('message_id', 
                #'conversation',
                'message_content',
                'timestamp',
                'read', 
                'sender_first_name',
                'parent_messages',
                )
    
    def validate_message_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message Body Cannot Be Empty")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'created_at',
            'participants',
            'messages'
            )
    def get_participants(self, obj):
        return UserSerializer(obj.participants.all()[:10], many = True).data
    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all()[:10], many = True).data
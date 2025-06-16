from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone
from .managers import UnreadMessagesManager

class MessageQuerySet(models.QuerySet):
    """Custom queryset for efficient message filtering."""
    def for_user(self, user):
        return self.filter(conversation__participants=user)
    def unread(self):
        return self.filter(read=False)

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True, help_text='The groups this user belongs to.', verbose_name='groups', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions', related_query_name='user')

    def save(self, *args, **kwargs):
        if self._state.adding and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        participant_names = ', '.join(user.username for user in self.participants.all())
        return f"Conversation {self.conversation_id} with {participant_names}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_body = models.TextField(max_length=5000, help_text="The body/content of the message")
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    read = models.BooleanField(default=False, help_text="Whether the recipients have read the message")
    edited = models.BooleanField(default=False, help_text="Whether the message was edited by the sender")
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', help_text="Link to the original message if this is a reply")

    objects = MessageQuerySet.as_manager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['timestamp']
        indexes = [models.Index(fields=['sender', 'receiver', 'conversation', 'timestamp'])]

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField(max_length=250)
    edited_at = models.DateTimeField(default=timezone.now, db_index=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-edited_at']
        indexes = [models.Index(fields=['message', 'edited_at'])]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    is_message_read = models.BooleanField(default=False, help_text="Whether the user has viewed this notification")

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'created_at'])]
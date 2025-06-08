from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='user',
    )

    def save(self, *args, **kwargs):
        if self._state.adding and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
class Conversation(models.Model):

    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    participants = models.ManyToManyField(to=User, related_name= 'conversations')
    
    def __str__(self):
        return f"Conversation {self.conversation_id} with {', '.join(user.username for user in self.participants.all())}" # type: ignore


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    conversation = models.ForeignKey(to = Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete= models.CASCADE, related_name='sent_messages')
    sent_at = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
    
    def __str__(self) -> str:
        return f"Message from {self.sender.username} at {self.sent_at}"
        


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
import uuid

from .managers import UnreadMessagesManager

# ==============================
# Custom User Model
# ==============================

class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    We add extra fields like phone_number, bio, and profile_image.
    We also override the primary key with a UUID.
    """
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )  # Unique identifier instead of default integer ID

    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True
    )  # User profile picture, optional

    # We need to redefine these to avoid conflicts with the custom user model
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
        """
        Override the default save method to hash the user's password
        only when the user is being created (not updated).
        """
        if self._state.adding and self.password:
            self.set_password(self.password)  # Securely hash password
        super().save(*args, **kwargs)


# ==============================
# Conversation Model
# ==============================

class Conversation(models.Model):
    """
    Represents a group chat or private chat between multiple users.
    Each conversation has a unique ID, timestamps, and participants.
    """
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Set only once when created
    updated_at = models.DateTimeField(auto_now=True)      # Updates every time the model is saved

    participants = models.ManyToManyField(
        to=User,
        related_name='conversations'
    )  # Users involved in this conversation

    def __str__(self):
        """
        Returns a readable name for admin or debugging.
        """
        participant_names = ', '.join(user.username for user in self.participants.all())  # type: ignore
        return f"Conversation {self.conversation_id} with {participant_names}"


# ==============================
# Message Model
# ==============================

class Message(models.Model):
    """
    Represents a message sent from one user to others in a conversation.
    Each message belongs to a conversation and has a sender, timestamp, content, and read status.
    """
    message_id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )

    conversation = models.ForeignKey(
        to=Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )  # Link to which conversation this message belongs

    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )  # Who sent the message

    sent_at = models.DateTimeField(auto_now_add=True)  # When the message was sent

    message_body = models.TextField()  # The actual text content of the message

    read = models.BooleanField(default=False)  # Whether the recipient(s) have read the message

    # Managers: default and custom
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager to get only unread messages

    def __str__(self) -> str:
        """
        Display message sender and timestamp in admin/debug views.
        """
        return f"Message from {self.sender.username} at {self.sent_at}"

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone
from .managers import UnreadMessagesManager

class MessageQuerySet(models.QuerySet):
    """Custom queryset methods for filtering messages."""
    def for_user(self, user):
        """
        Returns all messages where the user is the sender or receiver.
        """
        return self.filter(models.Q(sender=user) | models.Q(receiver=user))
    def unread(self):
        """
        Returns all unread messages.
        """
        return self.filter(read=False)

class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    Adds extra fields like phone_number, bio, and profile_image, with UUID as primary key.
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
        Override the default save method to hash the user's password only when created.
        """
        if self._state.adding and self.password:
            self.set_password(self.password)  # Securely hash password
        super().save(*args, **kwargs)

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
        participant_names = ', '.join(user.username for user in self.participants.all())
        return f"Conversation {self.conversation_id} with {participant_names}"

class Message(models.Model):
    """
    Represents a message sent within a conversation.
    Supports threading, edit tracking, and read status.
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

    receiver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text="The user who receives this message."
    )  # Who receives the message

    sent_at = models.DateTimeField(
        default=timezone.now,
        db_index=True  # Speeds up queries sorting by timestamp
    )  # When the message was sent

    message_content = models.TextField(
        max_length=5000,
        help_text="The body/content of the message"
    )  # The actual text content of the message

    read = models.BooleanField(
        default=False,
        help_text="Whether the recipient has read the message"
    )  # Whether the recipient(s) have read the message

    edited = models.BooleanField(
        default=False,
        help_text="Whether the message was edited by the sender"
    )  # Tracks whether the message has been edited

    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text="Link to the original message if this is a reply"
    )  # Supports replying to messages

    objects = MessageQuerySet.as_manager()  # Custom queryset
    unread = UnreadMessagesManager()        # Custom manager for unread messages

    class Meta:
        ordering = ['sent_at']  # Newer messages appear after older ones
        indexes = [
            models.Index(fields=['sender', 'receiver', 'sent_at']),
        ]

    def __str__(self) -> str:
        """
        Display message sender and timestamp in admin/debug views.
        """
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.sent_at}"

class MessageHistory(models.Model):
    """Stores historical versions of edited messages."""
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_history'
    )
    old_content = models.TextField(max_length=250)
    edited_at = models.DateTimeField(default=timezone.now, db_index=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-edited_at']
        indexes = [models.Index(fields=['message', 'edited_at'])]

class Notification(models.Model):
    """
    Stores notifications for users about new messages.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )
    is_message_read = models.BooleanField(
        default=False,
        help_text="Whether the user has viewed this notification"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
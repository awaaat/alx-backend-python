from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone
from .managers import UnreadMessagesManager

class ChatUser(AbstractUser):
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

    email = models.EmailField(null=False, blank=False, unique=True)
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
        related_name='users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
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
        default=uuid.uuid4
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Set only once when created
    updated_at = models.DateTimeField(auto_now=True)      # Updates every time the model is saved

    participants = models.ManyToManyField(
        to= ChatUser,
        related_name = 'conversations'
    )  # Users involved in this conversation

    def __str__(self):
        """
        Returns a readable name for admin or debugging.
        """
        participant_names = ', '.join(user.username for user in self.participants.all())  # type: ignore
        return f"Conversation {self.conversation_id} with {participant_names}"


class Message(models.Model):
    """
    Represents a chat message between two users.
    This includes features like tracking if the message is read,
    if it has been edited, and allowing replies (threading).
    """
    message_id = models.UUIDField(primary_key=True, 
                                default=uuid.uuid4)
    
    conversation = models.ForeignKey(
        to = Conversation, 
        on_delete= models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        ChatUser,
        on_delete=models.CASCADE,
        related_name='message_sender',
        help_text="The user who sent this message."
        )

    # The user receiving the message.
    receiver = models.ForeignKey(
        ChatUser,
        on_delete=models.CASCADE,
        related_name='message_receiver',
        help_text="The user who receives this message."
        )

    # The actual message content.
    message_content = models.TextField(
        max_length=5000,
        help_text="The body/content of the message.",
        null=False,
        blank=False
        )

    # When the message was sent.
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True  # Speeds up queries that sort or filter by timestamp.
        )

    # Tracks whether the recipient has read the message.
    read = models.BooleanField(
        default=False,
        help_text="Whether the recipient has read the message."
        )

    # Tracks whether the message has been edited after sending.
    edited = models.BooleanField(
        default=False,
        help_text="Whether the message was edited by the sender."
    )

    # Supports replying to messages by referencing a parent message.
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text="If this message is a reply, link it to the original message here."
    )

    # Attaches the custom queryset for convenient querying (e.g., unread messages).
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['timestamp']  # Newer messages appear after older ones.

        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
            # Example: speeds up looking for all messages between two users over time.
        ]


class Notification(models.Model):
    """
    Stores notifications for users.
    In a real-world example, this lets the app tell a user
    "You have a new message" without opening the message table every time.
    """
    notification_id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4
    )
    user = models.ForeignKey(
        to = ChatUser, 
        on_delete= models.CASCADE,
        help_text="The user who receives this notification."
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        help_text="The message that triggered this notification."
        )

    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True  # Allows quick sorting of notifications by newest.
        )

    read = models.BooleanField(
        default=False,
        help_text="Whether the user has viewed this notification."
        )

    class Meta:
        ordering = ['-created_at']  # Most recent notifications appear first.

        indexes = [
            models.Index(fields=['user', 'created_at']),
            # Helps quickly retrieve recent notifications for a user.
        ]

class MessageHistory(models.Model):
    """ Stores historical versions of edited messages . """
    message_history_id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4
    )
    message = models.ForeignKey(Message, 
                                on_delete= models.CASCADE, 
                                )
    old_content = models.TextField(max_length= 250)
    edited_at = models.DateTimeField(default=timezone.now, db_index= True)
    edited_by = models.ForeignKey(ChatUser, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        ordering = ['-edited_at']
        indexes = [models.Index(fields=['message', 'edited_at'])]
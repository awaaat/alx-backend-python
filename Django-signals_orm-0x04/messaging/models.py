from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Custom queryset methods to help with filtering messages easily.
class MessageQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Returns all messages where the user is either the sender or recipient.
        In a real chat app, this lets you quickly load all conversations a user is part of.
        """
        return self.filter(models.Q(sender=user) | models.Q(receiver=user))

    def unread(self):
        """
        Returns all unread messages.
        Useful for showing message notifications like "You have 3 unread messages".
        """
        return self.filter(is_read=False)


class Message(models.Model):
    """
    Represents a chat message between two users.
    This includes features like tracking if the message is read,
    if it has been edited, and allowing replies (threading).
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message."
        )

    # The user receiving the message.
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text="The user who receives this message."
        )

    # The actual message content.
    message_content = models.TextField(
        max_length=5000,
        help_text="The body/content of the message."
        )

    # When the message was sent.
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True  # Speeds up queries that sort or filter by timestamp.
        )

    # Tracks whether the recipient has read the message.
    is_read = models.BooleanField(
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
    objects = MessageQuerySet.as_manager()

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

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_notification',
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

    is_message_read = models.BooleanField(
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
    message = models.ForeignKey(Message, 
                                on_delete= models.CASCADE, 
                                related_name='message_history')
    old_content = models.TextField(max_length= 250)
    edited_at = models.DateTimeField(default=timezone.now, db_index= True)
    edited_by = models.ForeignKey(User, on_delete= models.CASCADE)
    class Meta:
        ordering = ['-edited_at']
        indexes = [models.Index(fields=['message', 'edited_at'])]
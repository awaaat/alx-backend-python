from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from .services import NotificationService

@receiver(post_save, sender=Message)
def handle_new_notifications(sender, instance, created, **kwargs):
    """
    Automatically creates a user notification whenever a new message is saved.

    What's happening here:
    - Django's `post_save` signal watches for new `Message` instances.
    - When someone sends a message (i.e., a Message is created), this function runs.
    - It uses the NotificationService to log a notification for the message's recipient.

    Real-world example:
    Imagine a chat app. When Alice sends Bob a message,
    this function makes sure Bob gets a "You have a new message!" alert.

    Why this is useful:
    - It's automatic — you don’t have to manually create notifications every time.
    - Keeps the logic separate and reusable by delegating work to `NotificationService`.
    - It’s fail-safe: only runs if a new message is actually created (not when edited).
    """
    if created:
        NotificationService.create_notification(message=instance)

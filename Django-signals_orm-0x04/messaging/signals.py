from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from .services import *


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
    
    """if created:
        NotificationService.create_notification(message=instance)
    if not created:
        Notification.objects.create()
    """

    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_save, sender=Message)
def handle_message_edits(sender, instance, **kwargs):
    """
    Checks if a message was edited after it was first created.
    
    Purpose:
    - This function listens for changes to any `Message` object.
    - If someone changes the content of an existing message (edits it),
    the system should keep a history of what the message said before the edit.
    
    How it works:
    - Django calls this function *after* any Message is saved (whether it’s new or edited).
    - The function tries to find the *old version* of the message in the database.
    - It compares the old message content to the new one.
    - If the content has changed, it saves the old content to a separate history log
    and marks the message as “edited.”
    
    Real-world example:
    - Imagine a user in a chat app sends “Hi”.
    - Then they change it to “Hello”.
    - This function detects that change, logs the original “Hi” in the history,
    and sets a flag saying the message was edited.
    
    Why this is useful:
    - Helps with transparency, moderation, or audit trails.
    - Prevents users from changing what they said without leaving a trace.
    """
    
    # Check if the message instance has a primary key (i.e., already exists in the database).
    #We can use teh service layer of just bypass it 
    """
    if instance.pk:
        try:
            # Retrieve the version of the message from before this save operation.
            old_message = Message.objects.get(pk=instance.pk)

            # Compare the old content with the current one.
            if old_message.message_content != instance.message_content:
                # If different, log the old content in message history.
                LogMessageHistoryService.log_edits(instance, old_message.message_content)

                # Mark the current message as edited.
                instance.edited = True
                # Save the updated 'edited' flag to the database.
                instance.save(update_fields=["edited"])

        except Message.DoesNotExist:
            # This could happen if the message was just created and not found in DB yet.
            # In that case, we do nothing.
            pass
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk = instance.pk)
            if old_message.message_content != instance.message_content:
                MessageHistory.objects.create(
                    message = instance,
                    old_content = old_message.message_content, 
                    edited_by = instance.sender
                )
                instance.edited = True
                instance.save(update_fields=["edited"])
        except Message.DoesNotExist:
            # This could happen if the message was just created and not found in DB yet.
            # In that case, we do nothing.
            pass 

##For this, we can also use a service layer or bypass it. 

#Option 1 for using service layer
""" 
@receiver(post_delete, sender = User)       
def handle_user_deletion(sender, instance, **kwargs):
    try:
        UserCleanUpService.clean_user_data(instance)
    except Exception:
        pass
"""
## Option 2, by-passing it

@receiver(post_delete, sender=User)
def delete_user_data(sender, instance, **kwargs):
    """
    Deletes all related data when a User is removed:
    - Messages sent or received by the user
    - Notifications addressed to the user
    - Message history entries for messages sent by the user
    - Message history entries edited by the user
    """
    try:
        # Delete messages where the user is the sender
        Message.objects.filter(sender=instance).delete()

        # Delete messages where the user is the receiver
        Message.objects.filter(receiver=instance).delete()

        # Delete notifications related to the user
        Notification.objects.filter(user=instance).delete()

        # Delete message history where the message was sent by the user
        MessageHistory.objects.filter(message__sender=instance).delete()

        # Delete message history entries that were edited by the user
        MessageHistory.objects.filter(edited_by=instance).delete()
    except Exception:
        pass


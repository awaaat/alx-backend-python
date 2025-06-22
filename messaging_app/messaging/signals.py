from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver 
from django.db.models import Q
from .models import Message, MessageHistory, ChatUser, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
        Creates a notification for the receiver when a new message is created.
    Args:
        sender (Model): The model class (Message).
        instance (Message): The specific Message instance being saved.
        created (bool): Indicates whether the instance was newly created.
    """
    if created:
        user=instance.receiver,
        message=instance,
        read=False

@receiver(pre_save, sender = Message)
def log_edits(sender, instance, **kwargs):
    """
    Log the old content of a message before it ’s updated ( Task 1).
    Args :
    sender : The model class ( Message )
    instance : The Message instance being saved
    """
    if instance.message_id:
        try:
            old_message = Message.objects.get(message_id = instance.message_id)
            if old_message:
                instance.edited = True
            MessageHistory.objects.create(
                message = instance, 
                old_content = old_message,
                edited_by = instance.sender
            )
        except Exception as e:
            pass

@receiver(post_delete, sender = ChatUser)      
def delete_user_data(sender, instance, **kwargs):
    """
    Cleans up messages, notifications, and message history when a user is deleted (Task 2).
    Args:
    sender (Model): The model class (ChatUser).
    instance (ChatUser): The specific ChatUser instance being deleted.
    """
    # Delete messages where the user is the sender or receiver
    Message.objects.filter(
        Q(sender = instance)|Q(receiver = instance)
        ).delete()
    Notification.objects.filter(user = instance).delete()
    MessageHistory.objects.filter(edited_by =  instance).delete()
    
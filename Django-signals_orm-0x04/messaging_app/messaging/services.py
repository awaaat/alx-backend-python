from django.db import transaction
from .models import Notification

class NotificationService:
    """
    Handles the creation of user notifications.
    This keeps business logic separate from models and signals,
    making the codebase easier to maintain and test.
    
    In real-world terms: 
    Think of this as the backend version of a personal assistant 
    who logs a "You got a new message!" alert whenever someone sends you a message.
    """

    @staticmethod
    @transaction.atomic  # Ensures everything inside happens completely or not at all (no partial updates).
    def create_notification(message):
        """
        Creates a new notification for the recipient of the message.

        Why use this?
        - Keeps signals simple by offloading logic here.
        - Centralizes the notification logic, so if rules change later 
        (e.g., notify only if the user is online), you edit in one place.
        
        Example scenario:
        A user sends a message — this function is called in response,
        and a new notification entry is added for the recipient.
        """
        return Notification.objects.create(
            user= message.recipient,  # Who should get notified
            message = message          # What the notification is about
        )

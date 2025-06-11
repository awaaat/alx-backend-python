from django.test import TestCase
from .models import User, Message, Notification


class NotificationSignalTests(TestCase):
    
    def setUp(self) -> None:
        self.sender = User.objects.create_user(username='AllanD', password='testPass123')
        self.recipient = User.objects.create_user(username='SherryD', password='testPass1234')
    
    def test_notification_on_message_creation(self):
        message  = Message.objects.create(
                    sender = self.sender,
                    recipient = self.recipient,
                    message_content = "Hello Mis., How are you Today"
                    )
        notification = Notification.objects.get(user = self.recipient,message = message)
        self . assertEqual (notification.user, self.recipient)
        self . assertFalse (notification.is_message_read)
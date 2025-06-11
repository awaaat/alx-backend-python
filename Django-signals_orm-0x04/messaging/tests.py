from django.test import TestCase
from .models import User, Message, Notification


class NotificationSignalTests(TestCase):
    
    def setUp(self) -> None:
        self.sender = User.objects.create_user(username='AllanD', password='testPass123')
        self.receiver = User.objects.create_user(username='SherryD', password='testPass1234')
    
    def test_notification_on_message_creation(self):
        message  = Message.objects.create(
                    sender = self.sender,
                    receiver = self.receiver,
                    message_content = "Hello Mis., How are you Today"
                    )
        notification = Notification.objects.get(user = self.receiver,message = message)
        self . assertEqual (notification.user, self.receiver)
        self . assertFalse (notification.is_message_read)
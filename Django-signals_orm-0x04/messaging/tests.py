from django.test import TestCase
from .models import User, Message, Notification, MessageHistory
from django.urls import reverse

class NotificationSignalTests(TestCase):
    """
    Tests related to automatic notification creation when a new message is sent.
    This verifies that the signal responsible for creating notifications works as expected.
    """

    def setUp(self) -> None:
        """
        This method runs before each test.
        It creates two users: a sender and a receiver to simulate message sending between them.
        """
        self.sender = User.objects.create_user(username='AllanD', password='testPass123')
        self.receiver = User.objects.create_user(username='SherryD', password='testPass1234')

    def test_notification_on_message_creation(self):
        """
        Verifies that when a new message is created, a corresponding notification is also created for the receiver.
        Also checks that the notification is marked as unread by default.
        """
        # Create a message from sender to receiver
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            message_content="Hello Mis., How are you Today"
        )

        # Try to fetch the notification that should be automatically created
        notification = Notification.objects.get(user=self.receiver, message=message)

        # Assert that the notification belongs to the correct user (receiver)
        self.assertEqual(notification.user, self.receiver)

        # Assert that the message notification is initially unread
        self.assertFalse(notification.is_message_read)


class MessageHistoryViewTest(TestCase):
    """
    Tests related to the message history view.
    Ensures that the edit history of a message is displayed properly.
    """

    def setUp(self) -> None:
        """
        Creates two users and a message between them.
        Also creates a history entry for that message to simulate an edit.
        """
        self.sender = User.objects.create_user(username='Allan', password="Allande123")
        self.receiver = User.objects.create_user(username="Man", password="Manuu124")

        # Create a new message from sender to receiver
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            message_content="Hello Buddy, you good? Original Version"
        )

        # Create a historical record for the message (e.g., a previous version)
        self.message_history = MessageHistory.objects.create(
            message=self.message,
            old_content="First original Version"
        )

    def test_message_history(self):
        """
        Logs in as the sender and accesses the message history page.
        Asserts that the page loads successfully and contains the old message version.
        """
        # Simulate user login
        self.client.login(username='Allan', password="Allande123")

        # Reverse the URL using the name given in urls.py and pass the message's ID
        url = reverse('message_history_view', args=[self.message.pk])

        # Perform GET request to fetch the message history page
        response = self.client.get(url)

        # Check if the page loaded successfully
        self.assertEqual(response.status_code, 200)

        # Ensure the old content is visible in the response HTML
        self.assertContains(response, "First original Version")

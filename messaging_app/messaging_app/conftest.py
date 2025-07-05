import pytest # type: ignore
from django.conf import settings
from django.test.utils import get_runner


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Pytest fixture that ensures database is set up for testing.
    This runs once per test session.
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_messaging_app',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }


@pytest.fixture
def api_client():
    """
    Fixture that provides a Django REST framework API client.
    """
    from rest_framework.test import APIClient # type: ignore
    return APIClient()


@pytest.fixture
def sample_users(db):
    """
    Fixture that creates sample users for testing.
    """
    from messaging.models import ChatUser
    
    sender = ChatUser.objects.create_user(
        username='testsender',
        password='testpass123',
        email='sender@test.com'
    )
    
    receiver = ChatUser.objects.create_user(
        username='testreceiver', 
        password='testpass123',
        email='receiver@test.com'
    )
    
    return {'sender': sender, 'receiver': receiver}


@pytest.fixture
def sample_message(db, sample_users):
    """
    Fixture that creates a sample message for testing.
    """
    from messaging.models import Message
    
    return Message.objects.create(
        sender=sample_users['sender'],
        receiver=sample_users['receiver'],
        message_content="Test message content"
    )
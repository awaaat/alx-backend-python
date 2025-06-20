from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from . import views

# Base router for top-level endpoints
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')  # Register UserViewSet under /users/
router.register(r'conversations', views.ConversationViewSet, basename='conversation')  # Register ConversationViewSet under /conversations/

# Nested router for conversation-specific messages
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation_id')  # Nest messages under /conversations/ with conversation_id as the lookup field
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')  # Register MessageViewSet under /conversations/<conversation_id>/messages/

# Nested router for user-specific conversations
user_router = NestedDefaultRouter(router, r'users', lookup='user_id')  # Nest conversations under /users/ with user_id as the lookup field
user_router.register(r'conversations', views.ConversationViewSet, basename='user-conversations')  # Register ConversationViewSet under /users/<user_id>/conversations/

# Consolidated urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include base router URLs (e.g., /users/, /conversations/)
    path('', include(conversations_router.urls)),  # Include nested router URLs for /conversations/<conversation_id>/messages/
    path('', include(user_router.urls)),  # Include nested router URLs for /users/<user_id>/conversations/
]


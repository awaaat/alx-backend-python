from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

# Base router for top-level endpoints
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')  # Changed 'user' to 'users' for clarity
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

# Nested router for conversation-specific messages
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')
conversations_router.register(r'users', views.UserViewSet, basename='conversation-participant')

# Nested router for user-specific messages and conversations
user_router = NestedDefaultRouter(router, r'users', lookup='user')
user_router.register(r'conversations', views.ConversationViewSet, basename='user-conversations')

# Consolidated urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('', include(user_router.urls)),
]
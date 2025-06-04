from django.urls import path, include
from .import views
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter # type: ignore

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

user_router = NestedDefaultRouter(router, r'user', lookup = 'user')
user_router.register(r'messages',  views.MessageViewSet, basename='user-messages')
user_router.register(r'conversations',  views.MessageViewSet, basename='user-conversations')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('', include(user_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
]

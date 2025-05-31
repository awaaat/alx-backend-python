from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserViewset)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('user/details/<str:first_name>/', views.UserDetailsView.as_view(), name = 'user-details'),
    path('messages/details/<uuid:message_id>/', views.MessageDetailsView.as_view(), name='message-details'),
    path('conversations/details/<uuid:conversation_id>/', views.ConversationDetailsView.as_view(), name='conversation_details'),
]
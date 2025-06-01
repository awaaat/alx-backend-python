from django.urls import path, include
from .import views
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter # type: ignore

router = routers.DefaultRouter()
router.register(r'user', views.UserViewset)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('user/details/<str:first_name>/', views.UserDetailsView.as_view(), name = 'user-details'),
    path('messages/details/<uuid:message_id>/', views.MessageDetailsView.as_view(), name='message-details'),
    path('conversations/details/<uuid:conversation_id>/', views.ConversationDetailsView.as_view(), name='conversation_details'),
]
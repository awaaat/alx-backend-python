from django.urls import path
from .views import message_history_view

urlpatterns = [
    path('messages/<int:message_id>/history/', message_history_view, name='message_history_view'),
]

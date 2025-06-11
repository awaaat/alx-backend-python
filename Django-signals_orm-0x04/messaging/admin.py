from django.contrib import admin
from .models import Notification, Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Custom admin display settings for the Message model.

    Why this matters:
    - Helps admins or moderators quickly review messages in the admin panel.
    - Makes it easier to filter, search, and scan through messages efficiently.
    """
    
    # Controls which fields show up in the admin list view
    list_display = ['sender', 'receiver', 'content_preview', 'timestamp']
    
    # Adds filters in the sidebar to narrow messages by time or read status
    list_filter = ['timestamp', 'is_read']
    
    # Enables a search bar to look up messages by their content
    search_fields = ['message_content']
    
    def content_preview(self, obj):
        """
        Displays a shortened version of the message content.

        Real-world benefit:
        Imagine you're an admin checking dozens of messages —
        instead of showing long texts, this previews the first 50 characters.
        """
        return obj.message_content[:50] + '...' if len(obj.message_content) > 50 else obj.message_content

    content_preview.short_description = "Preview"  # This sets a friendly column name in the admin UI

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Custom admin display settings for the Notification model.

    Why this is useful:
    - Lets admins easily track who received which notification, when,
    and whether they have read it.
    """
    
    list_display = ['user', 'message', 'created_at', 'is_message_read']
    list_filter = ['is_message_read', 'created_at']

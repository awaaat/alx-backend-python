from django.db import models
class UnreadMessagesManager(models.Manager):
    """
    Custom model manager for filtering unread messages for a specific user.

    This allows you to call something like:
    Message.unread.unread_for_user(current_user)
    to get all unread messages in conversations the user is part of.
    """

    def unread_for_user(self, user):
        """
        Return a queryset of unread messages that belong to any conversation
        where the specified user is a participant.

        Args:
            user (User): The user to fetch unread messages for.

        Returns:
            QuerySet: Unread Message objects, optimized for performance.
        """
        
        return self.get_queryset().filter(
            conversation__participant= user, read = False
        ).only(
            'message_id',
            'sender__username',
            'message_content',
            'send_at'
        ).select_related(
            'sender'  # Optimize query: fetch sender info in same DB call
        )

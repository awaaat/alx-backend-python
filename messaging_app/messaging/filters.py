from django_filters import rest_framework as filters  # type: ignore
from .models import Message, ChatUser

class MessageFilter(filters.FilterSet):
    """
    Filter class for the Message model.
    
    This class enables API clients to filter messages based on:
    - Sender: the user who sent the message
    - Time range: messages sent on or after a specific datetime (start)
    and/or on or before a specific datetime (end)
    
    Usage examples in API queries:
    - ?sender=5
    - ?sent_at__gte=2024-01-01T00:00
    - ?sent_at__lte=2024-12-31T23:59
    """
    
    # Filter by sender (must be a valid User object)
    sender = filters.ModelChoiceFilter(
        queryset= ChatUser.objects.all(),     # All users are available as filter choices
        field_name='sender',             # Filter field corresponds to the sender FK in Message
        label='Sender',                  # Optional UI/display label
    )
    
    # Filter messages created on or after a given datetime
    sent_at__gte = filters.DateTimeFilter(
        field_name='sent_at',            # Filter field corresponds to 'sent_at' datetime in Message
        lookup_expr='gte',               # 'gte' = greater than or equal to
        label='Sent at (greater than or equal)',  # Optional label
    )
    
    # Filter messages created on or before a given datetime
    sent_at__lte = filters.DateTimeFilter(
        field_name='sent_at',            # Filter field corresponds to 'sent_at' datetime in Message
        lookup_expr='lte',               # 'lte' = less than or equal to
        label='Sent at (less than or equal)',     
    )
    
    class Meta:
        """
        Meta configuration linking the filter set to the Message model.
        Declares which fields are available for filtering.
        """
        model = Message
        fields = ['sender', 'sent_at__gte', 'sent_at__lte']

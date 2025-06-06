from django_filters import rest_framework as filters # type: ignore
from .models import Message
from .models import User 
from typing import Type

class MessageFilter(filters.FilterSet):
    #filter by sender
    user = filters.ModelChoiceFilter(
                                queryset = User.objects.all(),
                                field_name = 'sender',
                                label = 'Sender',
                                )
    # Filter messages created on or after a given date
    start_date = filters.DateTimeFilter(
                                field_name = 'sent_at',
                                lookup_expr = 'gte',
                                label = 'Start Date'
                                )
    end_date = filters.DateTimeFilter(
                                field_name = 'sent_at',
                                lookup_expr = 'lte',
                                label = 'End Date',
                                )
    # Meta class to link filter to the Message model
    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
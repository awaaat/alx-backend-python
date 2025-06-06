from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    Limits API responses to 20 messages per page, as required.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
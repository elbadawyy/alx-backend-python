import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    sender = django_filters.NumberFilter(field_name="sender__id")

    class Meta:
        model = Message
        fields = ['sender', 'start', 'end']

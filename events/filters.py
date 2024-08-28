import django_filters
from django.utils import timezone

from events.models import Event


class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    type = django_filters.CharFilter(lookup_expr='icontains')
    created_by = django_filters.CharFilter(
        method='filter_created_by'
    )
    status = django_filters.ChoiceFilter(
        choices=[
            ('future', 'Future'),
            ('past', 'Past'),
            ('all', 'All'),
        ],
        method='filter_status',
    )

    class Meta:
        model = Event
        fields = ['date', 'type', 'status', 'created_by']

    def filter_status(self, queryset, name, value):
        now = timezone.now()
        if value == 'future':
            return queryset.filter(date__gt=now)
        elif value == 'past':
            return queryset.filter(date__lt=now)
        return queryset

    def filter_created_by(self, queryset, name, value):
        if value == 'my':
            user = self.request.user
            return queryset.filter(created_by=user)
        else:
            return queryset.filter(created_by__username__icontains=value)

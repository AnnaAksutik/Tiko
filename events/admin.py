from django.contrib import admin

from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_by', 'is_future_event')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('date', 'created_by')


admin.site.register(Event, EventAdmin)

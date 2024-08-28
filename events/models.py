from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    max_attendees = models.PositiveIntegerField(null=False, default=50)

    def __str__(self):
        return self.title

    @property
    def is_future_event(self):
        return self.date > timezone.now()

    @property
    def is_full(self):
        return self.attendees.count() >= self.max_attendees


from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from events.models import Event


class EventFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)

        self.now = timezone.now()
        self.future_event = Event.objects.create(
            title="Future Event",
            description="Future event description",
            type="Meeting",
            date=self.now + timezone.timedelta(days=1),
            created_by=self.user,
            max_attendees=10
        )
        self.past_event = Event.objects.create(
            title="Past Event",
            description="Past event description",
            type="Meeting",
            date=self.now - timezone.timedelta(days=1),
            created_by=self.user,
            max_attendees=10
        )

    def test_filter_future_events(self):
        response = self.client.get('/api/events/', {'status': 'future'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.json()
        titles = [event['title'] for event in events]
        self.assertIn(self.future_event.title, titles)
        self.assertNotIn(self.past_event.title, titles)

    def test_filter_past_events(self):
        response = self.client.get('/api/events/', {'status': 'past'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.json()
        titles = [event['title'] for event in events]
        self.assertIn(self.past_event.title, titles)
        self.assertNotIn(self.future_event.title, titles)

    def test_filter_all_events(self):
        response = self.client.get('/api/events/', {'status': 'all'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.json()  # Assuming response is a list
        titles = [event['title'] for event in events]
        self.assertIn(self.future_event.title, titles)
        self.assertIn(self.past_event.title, titles)

    def test_no_status_filter(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.json()  # Assuming response is a list
        titles = [event['title'] for event in events]
        self.assertIn(self.future_event.title, titles)
        self.assertIn(self.past_event.title, titles)

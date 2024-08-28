from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('events/<int:pk>/register/', EventViewSet.as_view({'post': 'register', 'delete': 'unregister'}), name='event_register'),
    path('', include(router.urls)),
]
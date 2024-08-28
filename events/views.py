from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event
from events.serializers import EventSerializer
from tiko.permissions import IsEventOwnerAndFuture


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventOwnerAndFuture]
    filterset_class = EventFilter

    def get_permissions(self):
        if self.action in ['register', 'unregister']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user in event.attendees.all():
            return Response({'detail': 'You are already registered for this event.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif event.is_full:
            return Response({'detail': 'This event is full. No more attendees can be added.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not event.is_future_event:
            return Response({'detail': 'You cannot register for a past event.'},
                            status=status.HTTP_400_BAD_REQUEST)

        event.attendees.add(user)
        return Response({'detail': 'Successfully registered for the event.'}, status=status.HTTP_200_OK)

    @register.mapping.delete
    def unregister(self, request, pk=None):
        event = self.get_object()
        user = request.user
        if not event.is_future_event:
            return Response({'detail': 'You cannot unregister for a past event.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif user not in event.attendees.all():
            return Response({'detail': 'You are not registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.remove(user)
        return Response({'detail': 'Successfully unregistered from the event.'}, status=status.HTTP_200_OK)

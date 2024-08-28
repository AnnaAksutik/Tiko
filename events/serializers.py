from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    attendees = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'type', 'description', 'date', 'created_by', 'attendees', 'max_attendees']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_attendees(self, obj):
        return [attendee.username for attendee in obj.attendees.all()]

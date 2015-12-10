from rest_framework import serializers
from django.utils import timezone
from smallslive.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    in_progress = serializers.SerializerMethodField('get_in_progress')

    class Meta:
        model = Event
        fields = ('title', 'start', 'end', 'photo', 'in_progress')

    def get_in_progress(self, obj):
        now = timezone.now()
        return obj.start <= now <= obj.end

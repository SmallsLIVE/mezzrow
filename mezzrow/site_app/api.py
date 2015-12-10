from rest_framework import generics
from smallslive.events.models import Event
from django.utils import timezone
import datetime
from .serializers import EventSerializer


class TodayEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        date_range_start = date_range_end = now
        if now.hour > 4:
            date_range_end += datetime.timedelta(days=1)
        date_range_end = date_range_end.replace(hour=6)
        events = Event.objects.filter(state=Event.STATUS.Published).filter(
            end__gte=date_range_start, end__lte=date_range_end)
        return events

todays_events = TodayEventsView.as_view()

from django.views.decorators.cache import cache_page
from django.utils import timezone
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from smallslive.events.models import Event
import datetime
from .serializers import EventSerializer


class TodayEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'events/events_api_list.html'

    def get(self, request, *args, **kwargs):
        res = super(TodayEventsView, self).get(request, *args, **kwargs)
        return Response({'events': self.object_list})

    def get_queryset(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())
        date_range_start = date_range_end = now
        if now.hour > 4:
            date_range_end += datetime.timedelta(days=1)
        date_range_end = date_range_end.replace(hour=6)
        events = Event.objects.filter(state=Event.STATUS.Published).filter(
            end__gte=date_range_start, end__lte=date_range_end).order_by('start')
        return events

todays_events = TodayEventsView.as_view()

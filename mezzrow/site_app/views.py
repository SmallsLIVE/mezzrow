from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from smallslive.events.models import Event


class HomeView(ListView):
    context_object_name = 'events'
    template_name = 'home.html'

    def get_queryset(self):
        return reversed(Event.objects.all().order_by('-start')[:20])

home_view = HomeView.as_view()


class EventDetailView(DetailView):
    context_object_name = 'event'
    model = Event
    template_name = 'event.html'

event_view = EventDetailView.as_view()


class AboutView(TemplateView):
    template_name = 'about.html'

about_view = AboutView.as_view()

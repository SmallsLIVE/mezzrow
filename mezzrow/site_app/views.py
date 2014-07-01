from django.core.urlresolvers import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.utils.timezone import datetime, timedelta
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from smallslive.artists.views import ArtistAddView as CoreArtistAddView
from smallslive.events.models import Event
from smallslive.events.views import EventAddView as CoreEventAddView


class HomeView(ListView):
    context_object_name = 'events'
    template_name = 'home.html'

    def get_queryset(self):
        #today = datetime.now().date()
        #few_days_out = today + timedelta(days=14)
        #return Event.objects.filter(start__range=(today, few_days_out)).reverse()
        return reversed(Event.objects.order_by('-start')[:20])

home_view = HomeView.as_view()


class EventDetailView(DetailView):
    context_object_name = 'event'
    model = Event
    template_name = 'event.html'

event_view = EventDetailView.as_view()


class AboutView(TemplateView):
    template_name = 'about.html'

about_view = AboutView.as_view()


class ContactView(TemplateView):
    template_name = "contact.html"

contact_view = ContactView.as_view()


class EventAddView(CoreEventAddView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_add = EventAddView.as_view()


class ArtistAddView(CoreArtistAddView):
    success_url = reverse_lazy('home')

artist_add = ArtistAddView.as_view()

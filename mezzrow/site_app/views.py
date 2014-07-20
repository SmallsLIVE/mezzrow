from django.core.urlresolvers import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from smallslive.artists.views import ArtistAddView as CoreArtistAddView
from smallslive.events.models import Event
from smallslive.events.views import EventAddView as CoreEventAddView, EventEditView as CoreEventEditView


class HomeView(ListView):
    context_object_name = 'events'
    template_name = 'home.html'

    def get_queryset(self):
        today = timezone.now().date()
        if self.request.user.is_superuser:
            events = Event.objects.filter(start__gte=today)
        else:
            few_days_out = today + timezone.timedelta(days=14)
            events = Event.objects.filter(start__range=(today, few_days_out), state=Event.STATUS.Published).reverse()
        return events.reverse()

# cache for 60 * 60 = 60 min
#home_view = cache_page(60 * 60)(HomeView.as_view())
home_view = HomeView.as_view()


class EventDetailView(DetailView):
    context_object_name = 'event'
    model = Event
    template_name = 'event.html'

# cache for 60 * 60 = 60 min
#event_view = cache_page(60 * 60)(EventDetailView.as_view())
event_view = EventDetailView.as_view()


class AboutView(TemplateView):
    template_name = 'about.html'

# cache for 60 * 60 * 24 = 86400s = 24 hours
#about_view = cache_page(60 * 60 * 24)(AboutView.as_view())
about_view = AboutView.as_view()


class ContactView(TemplateView):
    template_name = "contact.html"

# cache for 60 * 60 * 24 = 86400s = 24 hours
#contact_view = cache_page(60 * 60 * 24)(ContactView.as_view())
contact_view = ContactView.as_view()


class EventAddView(CoreEventAddView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_add = EventAddView.as_view()


class EventEditView(CoreEventEditView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_edit = EventEditView.as_view()


class ArtistAddView(CoreArtistAddView):
    success_url = reverse_lazy('home')

artist_add = ArtistAddView.as_view()

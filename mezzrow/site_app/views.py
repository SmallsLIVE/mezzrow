from braces import views
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from smallslive.artists.models import Artist
from smallslive.artists.views import ArtistAddView as CoreArtistAddView, ArtistEditView as CoreArtistEditView
from smallslive.events.models import Event
from smallslive.events.views import EventAddView as CoreEventAddView, EventEditView as CoreEventEditView
from .forms import EventEditForm


class HomeView(ListView):
    context_object_name = 'events'
    template_name = 'home.html'

    def get_queryset(self):
        """
        The view returns a list of events in two week intervals, for both the home page
        and the "next" links. The correct two week interval is set through the URL or by
        default it's a two week interval from the current date.

        """
        two_week_interval = int(self.kwargs.get('week', 0))
        date_range_start = timezone.now().date() + timezone.timedelta(days=two_week_interval*14)
        date_range_end = date_range_start + timezone.timedelta(days=(two_week_interval+1)*14)
        events = Event.objects.filter(start__range=(date_range_start, date_range_end))
        # only admin sees draft and hidden events
        if not self.request.user.is_superuser:
            events = events.filter(Q(state=Event.STATUS.Published) | Q(state=Event.STATUS.Cancelled))
        return events.reverse()

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        week = int(self.kwargs.get('week', 0))
        if week > 1:
            data['prev_url'] = reverse('next', kwargs={'week': week-1})
        elif week == 1:
            data['prev_url'] = reverse('home')
        # check if there are events in the next interval before showing the "next" link
        date_range_start = timezone.now().date() + timezone.timedelta(days=(week+1)*14)
        date_range_end = date_range_start + timezone.timedelta(days=(week+2)*14)
        next_events_exist = Event.objects.filter(start__range=(date_range_start, date_range_end)).exists()
        if next_events_exist:
            data['next_url'] = reverse('next', kwargs={'week': week+1})
        return data

# cache for 60 * 60 = 60 min
#home_view = cache_page(60 * 60)(HomeView.as_view())
home_view = HomeView.as_view()


class MonthView(HomeView):
    def get_queryset(self):
        today = timezone.now().date()
        return Event.objects.filter(Q(state=Event.STATUS.Published) | Q(state=Event.STATUS.Cancelled),
                                    start__gte=today,
                                    start__month=today.month,
                                    ).reverse()

# cache for 60 * 60 = 60 min
#month_view = cache_page(60 * 60)(MonthView.as_view())
month_view = MonthView.as_view()


class YearView(HomeView):
    def get_queryset(self):
        today = timezone.now().date()
        return Event.objects.filter(Q(state=Event.STATUS.Published) | Q(state=Event.STATUS.Cancelled),
                                    start__gte=today,
                                    start__year=today.year,
                                    ).reverse()

# cache for 60 * 60 = 60 min
#year_view = cache_page(60 * 60)(YearView.as_view())
year_view = YearView.as_view()


class EventDetailView(DetailView):
    context_object_name = 'event'
    model = Event
    template_name = 'events/event_detail.html'

# cache for 60 * 60 = 60 min
#event_view = cache_page(60 * 60)(EventDetailView.as_view())
event_view = EventDetailView.as_view()


class ArtistDetailView(DetailView):
    context_object_name = 'artist'
    model = Artist
    template_name = 'artists/artist_detail.html'

artist_view = ArtistDetailView.as_view()


class AboutView(TemplateView):
    template_name = 'about.html'

# cache for 60 * 60 * 24 = 86400s = 24 hours
about_view = cache_page(60 * 60 * 24)(AboutView.as_view())
#about_view = AboutView.as_view()


class ContactView(TemplateView):
    template_name = "contact.html"

# cache for 60 * 60 * 24 = 86400s = 24 hours
contact_view = cache_page(60 * 60 * 24)(ContactView.as_view())
#contact_view = ContactView.as_view()


class TicketingView(TemplateView):
    template_name = "ticketing.html"

# cache for 60 * 60 * 24 = 86400s = 24 hours
ticketing_view = cache_page(60 * 60 * 24)(TicketingView.as_view())
#ticketing_view = TicketingView.as_view()


class EventAddView(views.SuperuserRequiredMixin, CoreEventAddView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_add = EventAddView.as_view()


class EventEditView(views.SuperuserRequiredMixin, CoreEventEditView):
    form_class = EventEditForm

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_edit = EventEditView.as_view()


class EventDeleteView(views.SuperuserRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('home')

event_delete = EventDeleteView.as_view()


class ArtistAddView(views.SuperuserRequiredMixin, CoreArtistAddView):
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.full_name())})

artist_add = ArtistAddView.as_view()


class ArtistEditView(views.SuperuserRequiredMixin, CoreArtistEditView):
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.full_name())})

artist_edit = ArtistEditView.as_view()

import uuid
from braces import views
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.forms.formsets import all_valid
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from oscar.apps.catalogue.models import ProductImage
from oscar.apps.partner.models import StockRecord
from smallslive.artists.models import Artist
from smallslive.artists.views import ArtistAddView as CoreArtistAddView, ArtistEditView as CoreArtistEditView
from smallslive.events.models import Event
from smallslive.events.views import EventAddView as CoreEventAddView, EventEditView as CoreEventEditView,\
    EventCloneView as CoreEventCloneView
from .forms import TicketAddForm


class HomeView(ListView):
    context_object_name = 'events'
    template_name = 'home.html'

    def get_queryset(self):
        """
        The view returns a list of events in two week intervals, for both the home page
        and the "next" links. The correct two week interval is set through the URL or by
        default it's a two week interval from the current date. The admin user sees all events
        immediately, regardless of date intervals and event status.
        """
        events = Event.objects.all()
        if not self.request.user.is_superuser:
            two_week_interval = int(self.kwargs.get('week', 0))
            start_days = two_week_interval * 14
            date_range_start = timezone.now().date() + timezone.timedelta(days=start_days)
            # extra +1 at the end is to include the events on the last days when filtering on a DateTime field
            end_days = ((two_week_interval + 1) * 14) + 1
            date_range_end = date_range_start + timezone.timedelta(days=end_days)
            events = events.filter(start__range=(date_range_start, date_range_end))
            # only admin sees draft and hidden events
            events = events.filter(Q(state=Event.STATUS.Published) | Q(state=Event.STATUS.Cancelled))
        return events.reverse()

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            week = int(self.kwargs.get('week', 0))
            if week > 1:
                data['prev_url'] = reverse('next', kwargs={'week': week-1})
            elif week == 1:
                data['prev_url'] = reverse('home')
            # check if there are events in the next interval before showing the "next" link
            start_days = ((week + 1) * 14) + 1
            date_range_start = timezone.now().date() + timezone.timedelta(days=start_days)
            end_days = ((week + 2) * 14) + 1
            date_range_end = date_range_start + timezone.timedelta(days=end_days)
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
#about_view = cache_page(60 * 60 * 24)(AboutView.as_view())
about_view = AboutView.as_view()


class ContactView(TemplateView):
    template_name = "contact.html"

# cache for 60 * 60 = 86400s = 24 hours
#contact_view = cache_page(60 * 60)(ContactView.as_view())
contact_view = ContactView.as_view()


class TicketingView(TemplateView):
    template_name = "ticketing.html"

# cache for 60 * 60 * 24 = 86400s = 24 hours
#ticketing_view = cache_page(60 * 60 * 24)(TicketingView.as_view())
ticketing_view = TicketingView.as_view()


class EventAddView(views.SuperuserRequiredMixin, CoreEventAddView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inlines = self.construct_inlines()
        ticket_forms = self.construct_ticket_forms()
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines, ticket_forms=ticket_forms))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ticket_forms = self.construct_ticket_forms(data=request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)
            form_validated = True
        else:
            form_validated = False

        inlines = self.construct_inlines()

        if all_valid(inlines) and all_valid(ticket_forms) and form_validated:
            return self.forms_valid(form, inlines, ticket_forms)
        return self.forms_invalid(form, inlines, ticket_forms)

    def forms_valid(self, form, inlines, ticket_forms):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save()
        for formset in inlines:
            formset.save()
        for ticket in ticket_forms:
            if ticket.cleaned_data.get('form_enabled'):
                ticket.save(event=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, inlines, ticket_forms):
        """
        If the form or formsets are invalid, re-render the context data with the
        data-filled form and formsets and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines, ticket_forms=ticket_forms))

    def construct_ticket_forms(self, data=None):
        ticket_forms = []
        for i in range(1, settings.TICKETS_NUMBER_OF_SETS+1):
            ticket_form = TicketAddForm(data, prefix="set{0}".format(i), number=i)
            ticket_forms.append(ticket_form)
        return ticket_forms


event_add = EventAddView.as_view()


class EventEditView(views.SuperuserRequiredMixin, CoreEventEditView):
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.id, 'slug': slugify(self.object.title)})

event_edit = EventEditView.as_view()


class EventCloneView(CoreEventCloneView):
    def extra_event_processing(self, event, old_event_id):
        # clone the tickets
        old_event = Event.objects.get(id=old_event_id)
        for set_number, ticket in enumerate(old_event.products.all().order_by('id'), start=1):
            stock_record = ticket.stockrecord
            ticket.id = None
            ticket.event = event
            ticket.save()
            stock_record.id = None
            stock_record.product = ticket
            stock_record.num_in_stock = stock_record.initial_num_in_stock
            new_sku = "{0.month}-{0.day}-{0:%y}-{1}".format(event.start, set_number)
            # if that SKU exist for some reason, generate a random one that can be changed later manually
            sku_exists = StockRecord.objects.filter(partner_sku=new_sku).exists()
            if sku_exists:
                new_sku = uuid.uuid4().hex[:10]
            stock_record.partner_sku = new_sku
            stock_record.save()
            ProductImage.objects.create(product=ticket, original=event.photo)


event_clone = EventCloneView.as_view()


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

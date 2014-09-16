from operator import attrgetter
from collections import OrderedDict
from django.views.generic.detail import DetailView
from natsort import natsorted
from oscar.core.loading import get_class
from smallslive.events.models import Event

Line = get_class('order.models', 'Line')


class TicketDetailsView(DetailView):
    template_name = 'dashboard/ticket_details.html'
    context_object_name = 'event'
    model = Event

    def get_context_data(self, **kwargs):
        data = super(TicketDetailsView, self).get_context_data(**kwargs)
        sets = OrderedDict()
        products = list(self.object.products.all())
        products = natsorted(products, key=attrgetter('set'))
        for product in products:
            person_list = []
            for line in Line.objects.filter(product=product).exclude(
                    status="Cancelled").exclude(status="Exchanged").order_by('order__last_name'):
                person_list.append(line)
            sets[product.set] = person_list
        data['ticket_data'] = sets
        return data
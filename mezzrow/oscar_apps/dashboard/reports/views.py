from django.views.generic.detail import DetailView
from oscar.core.loading import get_class
from smallslive.events.models import Event

Order = get_class('order.models', 'Order')


class TicketDetailsView(DetailView):
    template_name = 'dashboard/ticket_details.html'
    context_object_name = 'event'
    model = Event

    def get_context_data(self, **kwargs):
        data = super(TicketDetailsView, self).get_context_data(**kwargs)
        sets = {}
        for product in self.object.products.all():
            person_list = []
            for order in Order.objects.filter(basket__lines__product=product).order_by('person_name'):
                person_list.append(order)
            sets[product.set] = person_list
        data['ticket_data'] = sets
        return data
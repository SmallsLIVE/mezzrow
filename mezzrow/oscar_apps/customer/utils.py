from django.conf import settings
from oscar.apps.customer.utils import Dispatcher as CoreDispatcher


class Dispatcher(CoreDispatcher):
    def dispatch_order_messages(self, order, messages, event_type=None,
                                **kwargs):
        # send a copy of the order message to the Mezzrow address
        self.send_email_messages(settings.ORDER_CONFIRMATION_COPY_EMAIL, messages)
        super(Dispatcher, self).dispatch_order_messages(order, messages, event_type, **kwargs)

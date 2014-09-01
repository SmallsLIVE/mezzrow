from oscar.apps.order.models import PaymentEventType
from oscar.apps.order.processing import EventHandler as CoreEventHandler


class EventHandler(CoreEventHandler):
    def handle_order_status_change(self, order, new_status):
        if new_status == "Cancelled":
            lines = order.lines.all()
            line_quantities = lines.values_list('quantity', flat=True)
            refund_event = PaymentEventType.objects.get(name="Refunded")
            self.handle_payment_event(order, refund_event, order.total_incl_tax, lines, line_quantities)
            self.cancel_stock_allocations(order, lines, line_quantities)
        order.set_status(new_status)

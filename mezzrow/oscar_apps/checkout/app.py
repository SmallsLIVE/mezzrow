from oscar.apps.checkout import app
from .views import PaymentDetailsView, IndexView


class CheckoutApplication(app.CheckoutApplication):
    payment_details_view = PaymentDetailsView
    index_view = IndexView


application = CheckoutApplication()

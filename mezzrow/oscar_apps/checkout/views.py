from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from oscar.apps.checkout import views
from oscar.apps.payment import forms, models
from oscar.core.loading import get_class

from paypal.payflow import facade

BankcardForm = get_class('payment.forms', 'BankcardForm')


class IndexView(views.IndexView):
    def form_valid(self, form):
        if form.is_guest_checkout():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            self.checkout_session.set_reservation_name(first_name, last_name)
        return super(IndexView, self).form_valid(form)


class PaymentDetailsView(views.PaymentDetailsView):

    def get_context_data(self, **kwargs):
        # Override method so the bankcard and billing address forms can be
        # added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get(
            'bankcard_form', BankcardForm())
        return ctx

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard/billingaddress submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = BankcardForm(request.POST)
        if not bankcard_form.is_valid():
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(
                bankcard_form=bankcard_form)
            return self.render_to_response(ctx)

        # Render preview with bankcard and billing address details hidden
        return self.render_preview(request,
                                   bankcard_form=bankcard_form)

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        bankcard_form = BankcardForm(request.POST)
        if not bankcard_form.is_valid():
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to PayPal
        """
        bankcard = kwargs['bankcard']
        facade.sale(
            order_number, total.incl_tax,
            bankcard)

        # Record payment source and event
        source_type, is_created = models.SourceType.objects.get_or_create(
            name='Credit Card')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=total.incl_tax, currency=total.currency,
            label=bankcard.number)
        self.add_payment_source(source)
        self.add_payment_event('Sold', total.incl_tax)
        
    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               order_total, payment_kwargs=None, order_kwargs=None):
        # if a registered user is making an order, copy his name to the order,
        # otherwise we're getting the reservation name from the guest user on the gateway form
        if not user.is_anonymous():
            first_name, last_name = user.first_name, user.last_name
        else:
            first_name, last_name = self.checkout_session.get_reservation_name()
        if not order_kwargs:
            order_kwargs = {}
        if first_name and last_name:
            order_kwargs.update({
                'first_name': first_name,
                'last_name': last_name
            })
        return super(PaymentDetailsView, self).submit(user, basket, shipping_address, shipping_method,
               order_total, payment_kwargs, order_kwargs)
from django import forms
from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm


class GatewayForm(CoreGatewayForm):
    reservation_name = forms.CharField(max_length=150, required=True,
                                       help_text="Name on the guest list for your reservation")

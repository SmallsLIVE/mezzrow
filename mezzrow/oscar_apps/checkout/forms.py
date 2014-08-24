from django import forms
from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm


class GatewayForm(CoreGatewayForm):
    first_name = forms.CharField(max_length=150, required=True,
                                       help_text="First name for the guest list")
    last_name = forms.CharField(max_length=150, required=True,
                                       help_text="Last name for the guest list")
    
    def clean(self):
        if not self.is_guest_checkout():
            if 'first_name' in self.errors:
                del self.errors['first_name']
            if 'last_name' in self.errors:
                del self.errors['last_name']
        return super(GatewayForm, self).clean()

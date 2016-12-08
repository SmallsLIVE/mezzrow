from django import forms
from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm
from oscar.apps.customer.utils import normalise_email
from email_validator import validate_email, EmailNotValidError

from django.utils.translation import ugettext_lazy as _
from oscar.core.compat import get_user_model
User = get_user_model()

class GatewayForm(CoreGatewayForm):
    username = forms.EmailField(required=True)
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
        if self.is_guest_checkout() or self.is_new_account_checkout():
            if 'password' in self.errors:
                del self.errors['password']
            if 'username' in self.cleaned_data:
                #
                # Overriding Oscar's built in GatewayForm cleaning that looks
                # for an existing account. This code is live by default in Oscar.
                #
                # email = normalise_email(self.cleaned_data['username'])
                # if User._default_manager.filter(email__iexact=email).exists():
                #     msg = _("A user with that email address already exists")
                #     self._errors["username"] = self.error_class([msg])
                pass
            return self.cleaned_data
        return super(GatewayForm, self).clean()

    def clean_username(self):
        email = normalise_email(self.cleaned_data['username'])
        try:
            v = validate_email(email)
            email = v["email"]
        except EmailNotValidError as e:
            raise forms.ValidationError("The email address is invalid. Perhaps there was a typo? Please try again.")
        return email

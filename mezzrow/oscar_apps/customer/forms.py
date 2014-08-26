from django import forms
from oscar.apps.customer.forms import EmailUserCreationForm as CoreEmailUserCreationForm


class EmailUserCreationForm(CoreEmailUserCreationForm):
    first_name = forms.CharField(max_length=150, required=True,
                                       help_text="First name of the user")
    last_name = forms.CharField(max_length=150, required=True,
                                       help_text="Last name of the user")

    class Meta(CoreEmailUserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        print self.fields['first_name']
        user = super(EmailUserCreationForm, self).save(commit=commit)
        print user.first_name
        return user
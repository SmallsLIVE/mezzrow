from oscar.apps.payment.forms import BankcardForm as CoreBankcardForm, Bankcard


class BankcardForm(CoreBankcardForm):
    fields = ('number', 'expiry_month', 'ccv')

    def __init__(self, *args, **kwargs):
        super(BankcardForm, self).__init__(*args, **kwargs)
        self.fields.pop('start_month')

    @property
    def bankcard(self):
        """
        Return an instance of the Bankcard model (unsaved)
        """
        return Bankcard(number=self.cleaned_data['number'],
                        expiry_date=self.cleaned_data['expiry_month'],
                        ccv=self.cleaned_data['ccv'])

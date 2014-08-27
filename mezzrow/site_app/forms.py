from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django import forms
from oscar.core.loading import get_class

Category = get_class('catalogue.models', 'Category')
Partner = get_class('partner.models', 'Partner')
Product = get_class('catalogue.models', 'Product')
ProductCategory = get_class('catalogue.models', 'ProductCategory')
ProductClass = get_class('catalogue.models', 'ProductClass')
StockRecord = get_class('partner.models', 'StockRecord')


class TicketAddForm(forms.Form):
    form_enabled = forms.BooleanField(initial=False, required=False)
    price = forms.DecimalField(label="Ticket price ($)", required=False)
    seats = forms.IntegerField(label="Number of seats", required=False)
    set_name = forms.CharField(max_length=50, label="Set name (example: Set 1: 9-11 PM)", required=False)

    class Meta:
        fields = ('price', 'seats', 'set_name')

    def __init__(self, *args, **kwargs):
        number = kwargs.pop('number', 1)
        super(TicketAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.layout = Layout(
            Field('form_enabled', css_class='toggle'),
            Div(
                Field('price'),
                Field('seats'),
                Field('set_name'),
                css_class='well'
            ),
        )
        self.fields['form_enabled'].label = "Add ticket to set {0}".format(number)

    def clean(self):
        cleaned_data = super(TicketAddForm, self).clean()
        form_enabled = cleaned_data.get('form_enabled', False)
        if form_enabled:
            price = cleaned_data.get('price')
            if not price:
                self._errors['price'] = self.error_class(["This field is required"])
            seats = cleaned_data.get('seats')
            if not seats:
                self._errors['seats'] = self.error_class(["This field is required"])
            set_name = cleaned_data.get('set_name')
            if not set_name:
                self._errors['set_name'] = self.error_class(["This field is required"])
        return cleaned_data

    def save(self, event):
        tickets_category, created = Category.objects.get_or_create(name="Tickets")
        product_class, created = ProductClass.objects.get_or_create(name="Tickets", requires_shipping=False)
        product = Product.objects.create(
            title=event.title,
            product_class=product_class,
            event_id=event.id,
            set=self.cleaned_data.get('set_name'),
        )
        ProductCategory.objects.create(
            product=product,
            category=tickets_category
        )
        partner, created = Partner.objects.get_or_create(name="Mezzrow")
        last_stockrecord = StockRecord.objects.order_by('-id').first()
        if last_stockrecord:
            last_id = last_stockrecord.id
        else:
            last_id = 0
        StockRecord.objects.create(
            partner=partner,
            product=product,
            partner_sku=last_id+1,
            num_in_stock=self.cleaned_data.get('seats'),
            price_excl_tax=self.cleaned_data.get('price'),
        )

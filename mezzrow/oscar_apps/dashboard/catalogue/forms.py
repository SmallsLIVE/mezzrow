from django.forms.widgets import TextInput
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm, ProductSelect


class ProductForm(CoreProductForm):
    class Meta(CoreProductForm.Meta):
        fields = ('title', 'event', 'set', 'is_discountable',)

        widgets = {
            'parent': ProductSelect,
            'event': TextInput,
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['event'].label = "Event ID"
        print self.fields

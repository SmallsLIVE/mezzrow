from crispy_forms.layout import Button
from smallslive.events.forms import EventAddForm


class EventEditForm(EventAddForm):
    def __init__(self, *args, **kwargs):
        super(EventEditForm, self).__init__(*args, **kwargs)
        self.helper.layout[-1].insert(1,
            Button('delete', 'Delete event', css_class="btn btn-danger",
                   data_toggle="modal", data_target="#deleteModal")
        )

from django.views.generic.list import ListView
from smallslive.events.models import Event


class HomeView(ListView):
    template_name = 'base.html'
    context_object_name = 'events'

    def get_queryset(self):
        return reversed(Event.objects.all().order_by('-start')[:20])

home_view = HomeView.as_view()

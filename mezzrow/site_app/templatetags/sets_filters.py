from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='set_times_filter')
def set_times_filter(value):
    print(value)
    a = value+timedelta(minutes = 90)
    return a

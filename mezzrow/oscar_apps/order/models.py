from django.db import models
from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    person_name = models.CharField(max_length=150, blank=True)

from oscar.apps.order.models import *
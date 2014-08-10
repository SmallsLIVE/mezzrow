from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):
    event = models.ForeignKey('events.Event', related_name='products', null=True)
    set = models.CharField(max_length=50, blank=True)

    class Meta(AbstractProduct.Meta):
        ordering = ['id', 'set', 'title']

from oscar.apps.catalogue.models import *

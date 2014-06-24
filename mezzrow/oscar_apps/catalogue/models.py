from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):
    event = models.ForeignKey('events.Event', related_name='products', null=True)

from oscar.apps.catalogue.models import *

from django.db import models
from oscar.apps.partner.abstract_models import AbstractStockRecord


class StockRecord(AbstractStockRecord):
    initial_num_in_stock = models.PositiveIntegerField("Initial number in stock", blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # When creating the stock record for the first time, remember the initial number of available products
        if not self.id:
            self.initial_num_in_stock = self.num_in_stock
        super(AbstractStockRecord, self).save(force_insert, force_update, using, update_fields)


from oscar.apps.partner.models import *

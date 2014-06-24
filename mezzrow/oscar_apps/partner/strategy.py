from oscar.apps.partner import availability, strategy
from .availability import MezzrowPolicy


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)


class Default(strategy.Default):
    def availability_policy(self, product, stockrecord):
        if not stockrecord:
            return availability.Unavailable()
        if not product.get_product_class().track_stock:
            return availability.Available()
        else:
            return MezzrowPolicy(
                stockrecord.net_stock_level)

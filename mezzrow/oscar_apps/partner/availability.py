from oscar.apps.partner.availability import StockRequired as CoreStockRequired


class MezzrowPolicy(CoreStockRequired):
    @property
    def message(self):
        if self.num_available > 0:
            return "{0} guaranteed seats available".format(self.num_available)
        return "Sold out - join wait list"

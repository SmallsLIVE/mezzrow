from oscar.apps.checkout.utils import CheckoutSessionData as CoreCheckoutSessionData


class CheckoutSessionData(CoreCheckoutSessionData):
    def set_reservation_name(self, name):
        self._set('guest', 'name', name)

    def get_reservation_name(self):
        return self._get('guest', 'name')

from django.test import TestCase
from oscar_apps.checkout.forms import GatewayForm

class TestForms(TestCase):

    def test_checkout_good_data(self):
        data = {
            'username' : 'test@user.com',
            'first_name' : 'Test',
            'last_name' : 'User',
            'options' : 'anonymous',
        }
        form = GatewayForm(data=data)
        self.assertTrue(form.is_valid())

    def test_checkout_bad_email(self):
        data = {
            'username' : 'test@user.con',
            'first_name' : 'Test',
            'last_name' : 'User',
            'options' : 'anonymous',
        }
        form = GatewayForm(data=data)
        self.assertFalse(form.is_valid())

    def test_checkout_bad_first(self):
        data = {
            'username' : 'test@user.com',
            'first_name' : 'TestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTestedTested',
            'last_name' : 'User',
            'options' : 'anonymous',
        }
        form = GatewayForm(data=data)
        self.assertFalse(form.is_valid())

    def test_checkout_bad_last(self):
        data = {
            'username' : 'test@user.com',
            'first_name' : 'Test',
            'last_name' : 'UsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsersUsers',
            'options' : 'anonymous',
        }
        form = GatewayForm(data=data)
        self.assertFalse(form.is_valid())

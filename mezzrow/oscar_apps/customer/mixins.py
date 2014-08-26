from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from oscar.apps.customer.mixins import RegisterUserMixin as CoreRegisterUserMixin
from oscar.apps.customer.signals import user_registered
from oscar.core.compat import get_user_model

User = get_user_model()


class RegisterUserMixin(CoreRegisterUserMixin):
    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        user = form.save()

        # Raise signal robustly (we don't want exceptions to crash the request
        # handling).
        user_registered.send_robust(
            sender=self, request=self.request, user=user)

        if getattr(settings, 'OSCAR_SEND_REGISTRATION_EMAIL', True):
            self.send_registration_email(user)

        # We have to authenticate before login
        try:
            user = authenticate(
                username=user.email,
                password=form.cleaned_data['password1'])
        except User.MultipleObjectsReturned:
            # Handle race condition where the registration request is made
            # multiple times in quick succession.  This leads to both requests
            # passing the uniqueness check and creating users (as the first one
            # hasn't committed when the second one runs the check).  We retain
            # the first one and delete the dupes.
            users = User.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.delete()

        auth_login(self.request, user)

        return user

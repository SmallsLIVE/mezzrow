"""
Django settings for mezzrow project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from smallslive.smallslive.settings.local_filip import *
from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from django.utils.translation import ugettext_lazy as _



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_1gqw#h-2%&9hnjh1f(ud43)w#%-454%ox)om0qm67c_6)(+g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.SmallsUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.twitter',
    'compressor',
    'crispy_forms',
    'debug_toolbar',
    'django_extensions',
    'django_thumbor',
    'djstripe',
    'floppyforms',
    'paypal',
    'pipeline',
    'sortedm2m',
    'south',
    'storages',
    'tinymce',

    # project apps
    'smallslive.artists',
    'smallslive.events',
    'smallslive.multimedia',
    'smallslive.old_site',
    'smallslive.users',
    'site_app'
] + get_core_apps([
    'catalogue',
    'checkout'
])

SITE_ID = 1

MIDDLEWARE_CLASSES += (
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.Emailbackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    OSCAR_MAIN_TEMPLATE_DIR,

)

TEMPLATE_CONTEXT_PROCESSORS += (
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mezzrow',
        'USER': 'bezidejni',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}


ROOT_URLCONF = 'mezzrow.urls'

WSGI_APPLICATION = 'mezzrow.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from oscar.defaults import *

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('PayPal'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('Express transactions'),
                'url_name': 'paypal-express-list',
            },
        ]
    })
"""
Django settings for mezzrow project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar import get_core_apps
from smallslive import SMALLSLIVE_TEMPLATE_DIR, SMALLSLIVE_STATIC_DIR
from smallslive.smallslive.settings.base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


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
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

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
    'corsheaders',
    'django_extensions',
    'django_thumbor',
    'floppyforms',
    'paypal',
    'rest_framework',
    #'pipeline',
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
    'oscar_apps.catalogue',
    'oscar_apps.checkout',
    'oscar_apps.customer',
    'oscar_apps.dashboard.catalogue',
    'oscar_apps.dashboard.orders',
    'oscar_apps.dashboard.reports',
    'oscar_apps.order',
    'oscar_apps.partner',
    'oscar_apps.payment'
])

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware'
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

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
    SMALLSLIVE_TEMPLATE_DIR,

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
    SMALLSLIVE_STATIC_DIR,
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ROOT_URLCONF = 'mezzrow.urls'

WSGI_APPLICATION = 'mezzrow.wsgi.application'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
AWS_S3_CUSTOM_DOMAIN = None

SHOW_TIMES = {
    # Starts with Monday
    "1": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-1:00", "After hours", "11:00 PM - 1:00 AM"),
    ),
    "2": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-1:00", "After hours", "11:00 PM - 1:00 AM"),
    ),
    "3": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-1:00", "After hours", "11:00 PM - 1:00 AM"),
    ),
    "4": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-1:00", "After hours", "11:00 PM - 1:00 AM"),
    ),
    "5": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-1:00", "After hours", "11:00 PM - 1:00 AM"),
    ),
    "6": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-0:00", "After hours", "11:00 PM - 12:00 AM"),
    ),
    "7": (
        ("16:30-19:00", "Early show", "4:30 PM - 7:00 PM"),
        ("20:00-22:30", "Main show", "8:00 PM - 10:30 PM"),
        ("23:00-0:00", "After hours", "11:00 PM - 12:00 AM"),
    ),
}
TICKETS_NUMBER_OF_SETS = 4
ORDER_CONFIRMATION_COPY_EMAIL = 'mezzrowclub@gmail.com'


# Paypal express
PAYPAL_API_USERNAME = os.environ.get("PAYPAL_API_USERNAME")
PAYPAL_API_PASSWORD = os.environ.get("PAYPAL_API_PASSWORD")
PAYPAL_API_SIGNATURE = os.environ.get("PAYPAL_API_SIGNATURE")
PAYPAL_SANDBOX_MODE = True
PAYPAL_CALLBACK_HTTPS = False
PAYPAL_API_VERSION = '88.0'
PAYPAL_CURRENCY = PAYPAL_PAYFLOW_CURRENCY = 'USD'
PAYPAL_PAYFLOW_COLOR = 'F26F40'

# Paypal PayFlow Pro
PAYPAL_PAYFLOW_VENDOR_ID = os.environ.get('PAYPAL_PAYFLOW_VENDOR_ID')
PAYPAL_PAYFLOW_USER = os.environ.get('PAYPAL_PAYFLOW_USER')
PAYPAL_PAYFLOW_PASSWORD = os.environ.get('PAYPAL_PAYFLOW_PASSWORD')
PAYPAL_PAYFLOW_PRODUCTION_MODE = False
PAYPAL_PAYFLOW_DASHBOARD_FORMS = True

from oscar.defaults import *

OSCAR_SHOP_NAME = 'Mezzrow'
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_REQUIRED_ADDRESS_FIELDS = None
OSCAR_FROM_EMAIL = 'mezzrowclub@mezzrow.com'

OSCAR_INITIAL_ORDER_STATUS = 'Completed'
OSCAR_INITIAL_LINE_STATUS = 'Completed'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Completed': ('Cancelled', 'Exchanged'),
    'Cancelled': (),
}
OSCAR_LINE_STATUS_PIPELINE = OSCAR_ORDER_STATUS_PIPELINE
OSCAR_ORDER_STATUS_CASCADE = {
    'Cancelled': 'Cancelled'
}

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('PayPal'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('Express transactions'),
                'url_name': 'paypal-express-list',
            },
            {
                'label': 'Payflow transactions',
                'url_name': 'paypal-payflow-list',
            }
        ]
    })

from .base import *

INSTALLED_APPS += (
    'debug_toolbar',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

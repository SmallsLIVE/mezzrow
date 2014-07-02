from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mezzrow',
        'USER': 'luke',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

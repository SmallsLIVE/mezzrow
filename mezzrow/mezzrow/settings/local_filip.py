from .local_base import *

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

INSTALLED_APPS += (
    'devserver',
)

CACHES= {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
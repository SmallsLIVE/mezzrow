import sys
from .local_base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mezzrow',
        'USER': 'jamessam',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

CACHES= {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

from .yo import *

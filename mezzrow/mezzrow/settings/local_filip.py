import sys
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

CACHES= {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

#CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
        'www.smallslive.com',
)
CORS_URLS_REGEX = r'^/api/.*$'
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin: *',
)

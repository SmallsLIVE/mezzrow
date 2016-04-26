import os
import dj_database_url
import sys
from .base import *


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val

SECRET_KEY = env_var("SECRET_KEY", "herokudefault")
DEBUG = env_var("DEBUG", False)

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
#DATABASES['default']['ENGINE'] = 'django_postgrespool'
DATABASES['default']['CONN_MAX_AGE'] = 300
# SOUTH_DATABASE_ADAPTERS = {
#     'default': 'south.db.postgresql_psycopg2'
# }
# DATABASE_POOL_ARGS = {
#     'max_overflow': 10,
#     'pool_size': 10,
#     'recycle': 300
#}


# Allow all host headers
ALLOWED_HOSTS = [
    'www.mezzrow.com',
    'www.mezzrow.com.',
    'mezzrow.com',
    'mezzrow.com.',
    'mezzrow-prod.herokuapp.com',
    'mezzrow-prod.herokuapp.com.',
]

# Memcached
# CACHES = {
#     'default': {
#         #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#         'BACKEND': 'django_bmemcached.memcached.BMemcached',
#         'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
#         'OPTIONS': {
#             'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
#             'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
#         }
#     },
#     'staticfiles': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'TIMEOUT': 60 * 60 * 24 * 365,
#         'LOCATION': 'staticfiles-filehashes'
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_SECONDS = 300
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = os.environ.get('STATIC_URL')
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
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
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'oscar': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

# Sentry
RAVEN_CONFIG = {
    'dsn': os.environ.get("SENTRY_DSN"),
}

INSTALLED_APPS += (
    'djrill',
    'loaderio',
    'raven.contrib.django.raven_compat',

)
MANDRILL_API_KEY = os.environ.get("MANDRILL_API_KEY")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
DEFAULT_FROM_EMAIL = "mezzrowclub@mezzrow.com"


# Security
MIDDLEWARE_CLASSES = ('sslify.middleware.SSLifyMiddleware',) + MIDDLEWARE_CLASSES
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Paypal express
PAYPAL_SANDBOX_MODE = False
PAYPAL_CALLBACK_HTTPS = True

# Paypal PayFlow Pro
PAYPAL_PAYFLOW_PRODUCTION_MODE = True

# CORS
CORS_ORIGIN_WHITELIST = (
        'www.smallslive.com',
)
CORS_URLS_REGEX = r'^/api/.*$'
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin: *',
)

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
DATABASES['default']['CONN_MAX_AGE'] = 30

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
CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
        'OPTIONS': {
            'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
            'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
        }
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
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

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
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        }
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
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
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
    'raven.contrib.django.raven_compat',

)
MANDRILL_API_KEY = os.environ.get("MANDRILL_API_KEY")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"


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

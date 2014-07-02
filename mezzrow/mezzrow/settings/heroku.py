import os
import dj_database_url
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

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

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
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Static asset configuration
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

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

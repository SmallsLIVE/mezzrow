"""
WSGI config for mezzrow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mezzrow.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import MediaCling
from .wsgi_static import MezzrowCling

application = MezzrowCling(MediaCling(get_wsgi_application()))

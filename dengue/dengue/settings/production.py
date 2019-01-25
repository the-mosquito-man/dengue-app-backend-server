import os

from django.core.exceptions import ImproperlyConfigured

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# MIDDLEWARE
MIDDLEWARE += [
    'django.middleware.csrf.CsrfViewMiddleware',
]
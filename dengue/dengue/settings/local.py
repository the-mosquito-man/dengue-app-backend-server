import json

from .base import *

from django.core.exceptions import ImproperlyConfigured

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# MIDDLEWARE
MIDDLEWARE += []

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dengue_db',
        'USER': 'dengue_user',
        'PASSWORD': 'dengue',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Secret key
with open(".secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the enviroment variable or return exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} enviroment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

AWS_ACCESS_KEY = get_secret("AWS_ACCESS_KEY")
AWS_SECRET_KEY = get_secret("AWS_SECRET_KEY")

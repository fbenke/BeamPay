import os

import dj_database_url

# ==================== GENERIC SETTINGS  ====================

BASE_DIR = lambda *x: os.path.join(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)).
    replace('\\', '/'), *x)


DEBUG = bool(int(os.environ.get('DEBUG', '1')))

TEMPLATE_DEBUG = bool(int(os.environ.get('TEMPLATE_DEBUG', '1')))

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

ENV = os.environ.get('ENV')
ENV_LOCAL = 'local'

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'corsheaders',
)

LOCAL_APPS = (
    'beam_value',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# SSL Redirects
if ENV != ENV_LOCAL:
    PROTOCOL = 'https'
    PRODUCTION_MIDDLEWARE = ('sslify.middleware.SSLifyMiddleware',)
else:
    PROTOCOL = 'http'
    # No automatic redirects on local
    PRODUCTION_MIDDLEWARE = ()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
)

ROOT_URLCONF = 'beam_value.urls'

WSGI_APPLICATION = 'beam_value.wsgi.application'

# Database

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files

STATIC_ROOT = 'static'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR('assets'),
)

TEMPLATE_DIRS = (
    BASE_DIR('templates'),
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

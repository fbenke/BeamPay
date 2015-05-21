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

# Environment descriptions
ENV_LOCAL = 'local'
ENV_DEV = 'dev'
ENV_VIP = 'vip'
ENV_PROD = 'prod'

ENV = os.environ.get('ENV')

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'userena',
    'guardian',
    'easy_thumbnails',
    'social.apps.django_app.default',
)

LOCAL_APPS = (
    'beam_value',
    'account',
    'pricing',
    'recipient'
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

# Site types in Env
SITE_API = 0
SITE_USER = 1

# ENV to URL mapping
ENV_SITE_MAPPING = {
    ENV_LOCAL: {
        SITE_API: os.environ.get('LOCAL_SITE_API'),
        SITE_USER: os.environ.get('LOCAL_SITE_USER'),
    },
    ENV_DEV: {
        SITE_API: 'api-dev.beampay.co',
        SITE_USER: 'dev.beampay.co',
    },
    ENV_VIP: {
        SITE_API: 'api-vip.beampay.co',
        SITE_USER: 'vip.beampay.co',
    },
    ENV_PROD: {
        SITE_API: 'api.beampay.co',
        SITE_USER: 'beampay.co',
    }
}

ROOT_URLCONF = 'beam_value.urls'

WSGI_APPLICATION = 'beam_value.wsgi.application'

DATABASES = {
    'default': dj_database_url.config()
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

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

# Django CORS headers
CORS_ORIGIN_WHITELIST = (ENV_SITE_MAPPING[ENV][SITE_USER], )
CORS_ALLOW_CREDENTIALS = True

# URL contruction
API_BASE_URL = PROTOCOL + '://' + ENV_SITE_MAPPING[ENV][SITE_API] + '/'
USER_BASE_URL = PROTOCOL + '://' + ENV_SITE_MAPPING[ENV][SITE_USER] + '/'


# ====================  Django Rest Framework ====================

REST_FRAMEWORK = {
    # if not specified otherwise, anyone can acess a view (this is the default)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    # if required, which authentication is eligible?
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # input formats the API can handle
    'DEFAULT_PARSER_CLASSES': (
        'beam_value.utils.parsers.CamelCaseJSONParser',
        # 'djangorestframework_camel_case.parser.CamelCaseJSONParser'
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    #  output format supported by the API
    'DEFAULT_RENDERER_CLASSES': (
        'beam_value.utils.renderers.CamelCaseJSONRenderer',
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # throttling of requests
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/second'
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# ==================== USERENA SETTINGS ====================

AUTHENTICATION_BACKENDS = (
    # Userena
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',

    # Facebook Graph
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2'
)

AUTH_PROFILE_MODULE = 'account.BeamProfile'
USERENA_WITHOUT_USERNAMES = True
USERENA_ACTIVATION_DAYS = 1
USERENA_USE_HTTPS = (ENV != ENV_LOCAL)

# disable userena admin customizations to allow our own ones
USERENA_REGISTER_USER = False
USERENA_REGISTER_PROFILE = False
USERENA_HTML_EMAIL = True
ANONYMOUS_USER_ID = -1

PASSWORD_REGEX = r'^(?=.*\d).{8,}$'

# ==================== PYTHON SOCIAL SETTINGS ================

# Facebook, http://python-social-auth.readthedocs.org/en/latest/backends/facebook.html
SOCIAL_AUTH_FACEBOOK = 'facebook'
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')

# if we ever decide to store the scope and app_id in one place, uncomment the
# following two statements and write an API call for those
# SOCIAL_AUTH_FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'profile']

# if we ever want to retrieve age_range uncomment the following
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'fields': 'age_range, first_name, last_name, verified, name,'
#     'locale, gender, email, link, timezone, updated_time'
# }

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    # Associates the current social details with another user account with
    # a similar email address. Deactivated by default.
    'social.pipeline.social_auth.associate_by_email',
    # Make sure that social account is verfified
    'account.social_auth.reject_no_email',
    # Make sure that social account has provided an email
    'account.social_auth.reject_not_verified',
    'social.pipeline.user.create_user',
    # Create and populate a profile with available data, if it has not happened yet
    'account.social_auth.save_profile',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# ==================== Email Settings ====================

if ENV in (ENV_LOCAL,):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'beam_value.utils.sendgrid_django.SendGridBackend'
    SENDGRID_USER = os.environ.get('SENDGRID_USERNAME')
    SENDGRID_PASSWORD = os.environ.get('SENDGRID_PASSWORD')

BEAM_MAIL_ADDRESS = 'Beam <hello@beampay.co>'
BEAM_SUPPORT_MAIL_ADDRESS = 'hello@beampay.co'
# ==================== User Email templates ====================

MAIL_ACTIVATION_SUBJECT = 'userena/emails/activation_email_subject.txt'
MAIL_ACTIVATION_TEXT = 'userena/emails/activation_email_message.txt'
MAIL_ACTIVATION_HTML = 'userena/emails/activation_email_message.html'
MAIL_PASSWORD_RESET_SUBJECT = 'userena/emails/password_reset_subject.txt'
MAIL_PASSWORD_RESET_TEXT = 'userena/emails/password_reset_message.txt'
MAIL_PASSWORD_RESET_HTML = 'userena/emails/password_reset_message.html'
MAIL_CHANGE_EMAIL_OLD_SUBJECT = 'userena/emails/confirmation_email_subject_old.txt'
MAIL_CHANGE_EMAIL_OLD_TEXT = 'userena/emails/confirmation_email_message_old.txt'
MAIL_CHANGE_EMAIL_OLD_HTML = 'userena/emails/confirmation_email_message_old.html'
MAIL_CHANGE_EMAIL_NEW_SUBJECT = 'userena/emails/confirmation_email_subject_new.txt'
MAIL_CHANGE_EMAIL_NEW_TEXT = 'userena/emails/confirmation_email_message_new.txt'
MAIL_CHANGE_EMAIL_NEW_HTML = 'userena/emails/confirmation_email_message_new.html'


# User-Facing URLs in Email templates
MAIL_ACTIVATION_URL = '#!/auth/activate/{}/'
MAIL_EMAIL_CHANGE_CONFIRM_URL = '#!/auth/settings/email/{}/'
MAIL_PASSWORD_RESET_URL = '#!/auth/forgot/{}-{}/'


# ==================== IP-based blocking ====================

COUNTRY_BLACKLIST = (
    # FATF Blacklist as of June 2014
    # see http://en.wikipedia.org/wiki/FATF_blacklist
    'IR',  # Iran
    'KP',  # North Korea
    'DZ',  # Algeria
    'EC',  # Ecuador
    'ID',  # Indonesia
    'MM',  # Myanmar
)

# TODO: activate once the site mapping for Angular/Django is complete
TOR_BLOCKING = False
TOR_TIMEOUT = 5

GEOIP_PATH = BASE_DIR('static', 'geo_data', 'GeoIP.dat')

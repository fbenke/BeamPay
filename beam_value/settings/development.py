from beam_value.settings.production import *

import logging


# store mails in memory to access them in unit tests
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

logging.disable(logging.CRITICAL)

# debug toolbar
INSTALLED_APPS += ('debug_toolbar',)

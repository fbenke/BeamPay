from django.contrib.auth.models import User
from django.db import models

from userena import settings as userena_settings
from userena.models import UserenaBaseProfile

from django_countries.fields import CountryField


class BeamProfile(UserenaBaseProfile):
    ''' represents a sender user profile '''

    user = models.OneToOneField(
        User,
        unique=True,
        related_name='profile'
    )

    country = CountryField(
        'Country',
        blank=True,
        help_text='Country'
    )

    accepted_privacy_policy = models.BooleanField(
        'Privacy Policy accepted',
        default=True
    )

    @property
    def account_deactivated(self):
        return (self.user.userena_signup.activation_key == userena_settings.USERENA_ACTIVATED
                and not self.user.is_active)

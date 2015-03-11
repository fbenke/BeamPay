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

    date_of_birth = models.DateField(
        'Date of Birth',
        null=True,
        blank=True,
        help_text='Date of birth'
    )

    phone_number = models.CharField(
        'Mobile Money Phone Number',
        max_length=15,
        blank=True,
        help_text='Phone number'
    )

    country = CountryField(
        'Country',
        null=True,
        blank=True,
        help_text='Country'
    )

    accepted_privacy_policy = models.BooleanField(
        'Privacy policy accepted',
        default=True
    )

    @property
    def account_deactivated(self):
        return (self.user.userena_signup.activation_key == userena_settings.USERENA_ACTIVATED
                and not self.user.is_active)

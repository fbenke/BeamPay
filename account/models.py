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
        'Phone Number',
        max_length=15,
        blank=True,
        help_text='Phone number'
    )

    street = models.CharField(
        'Street and number',
        max_length=50,
        blank=True,
        help_text='Street and number'
    )

    post_code = models.CharField(
        'Post Code',
        max_length=50,
        blank=True,
        help_text='Post Code'
    )

    city = models.CharField(
        'City',
        max_length=40,
        blank=True,
        help_text='City'
    )

    country = CountryField(
        'Country',
        null=True,
        blank=True,
        help_text='Country of Current Residence'
    )

    accepted_privacy_policy = models.BooleanField(
        'Privacy policy accepted',
        default=True
    )

    gender = models.CharField(
        'Gender',
        max_length=15,
        blank=True,
        help_text='Gender'
    )

    facebook_link = models.CharField(
        'Facebook Link',
        max_length=100,
        blank=True,
        help_text='Link to Facebook Profile'
    )

    @property
    def account_deactivated(self):
        return (self.user.userena_signup.activation_key == userena_settings.USERENA_ACTIVATED
                and not self.user.is_active)

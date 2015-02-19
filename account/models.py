from django.contrib.auth.models import User
from django.db import models

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

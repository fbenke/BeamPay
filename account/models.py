from django.contrib.auth.models import User
from django.db import models

from userena import settings as userena_settings
from userena.models import UserenaBaseProfile

from django_countries.fields import CountryField


class BeamProfile(UserenaBaseProfile):
    ''' represents a sender user profile '''

    PHONE = 'PHON'
    EMAIL = 'MAIL'
    SMS = 'SMS'
    WHATSAPP = 'WAP'

    CONTACT_METHODS = (PHONE, EMAIL, SMS, WHATSAPP)

    CONTACT_METHOD_CHOICES = (
        (PHONE, 'phone call'),
        (EMAIL, 'email'),
        (SMS, 'sms'),
        (WHATSAPP, 'whatsapp')
    )

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

    preferred_contact_method = models.CharField(
        'Preferred Contact Method',
        max_length=4,
        choices=CONTACT_METHOD_CHOICES,
        default=PHONE,
        help_text='Preferred Contact Method'
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

    @property
    def information_complete(self):
        if (
            self.user.email == '' or self.user.first_name == '' or
            self.user.last_name == '' or not self.user.is_active or
            self.date_of_birth is None or self.date_of_birth == '' or
            self.phone_number == '' or self.street == '' or
            self.post_code == '' or self.city == '' or
            self.country is None or self.country == ''
        ):
            return False
        return True

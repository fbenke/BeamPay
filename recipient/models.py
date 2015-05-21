from django.contrib.auth.models import User
from django.db import models


class Recipient(models.Model):

    PARENTS = 'PAR'
    SIBLING = 'SIB'
    FRIEND = 'FRD'
    UNSPECIFIED = 'USP'

    RELATION_CHOICES = (
        (PARENTS, 'parent'),
        (SIBLING, 'sibling'),
        (FRIEND, 'friend'),
        (UNSPECIFIED, 'not provided')
    )

    user = models.ForeignKey(
        User,
        unique=True,
        related_name='recipients'
    )

    first_name = models.CharField(
        'First Name',
        max_length=50,
        help_text='First name of recipient'
    )

    last_name = models.CharField(
        'Full Name',
        max_length=50,
        help_text='Last name of recipient'
    )

    phone_number = models.CharField(
        'Mobile Money Phone Number',
        max_length=15,
        help_text='Phone number of recipient'
    )

    email = models.EmailField(
        'Email',
        blank=True,
        help_text='Email of recipient'
    )

    date_of_birth = models.DateField(
        'Date of Birth',
        null=True,
        blank=True,
        help_text='Date of birth'
    )

    relation = models.CharField(
        'Relation between user and recipients',
        max_length=3,
        choices=RELATION_CHOICES,
        default=UNSPECIFIED,
        help_text='Relation between user and recipient'
    )

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

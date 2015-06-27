from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from referral.utils import generate_referral_code


def create_referral_code(user):

    referral = Referral.objects.create(
        user=user,
        code=generate_referral_code()
    )

    referral.save()


class Referral(models.Model):

    user = models.OneToOneField(
        User,
        unique=True,
        related_name='referral'
    )

    referred = models.ManyToManyField(
        'self',
        null=True,
        related_name='referer'
    )

    code = models.CharField(
        'Referral code',
        max_length=50,
        help_text='Referral code'
    )

    credits_gained = models.IntegerField(
        'Credits gained',
        default=0,
        help_text='How many credits did the user gain through referrals?'
    )

    credits_redeemed = models.IntegerField(
        'Credits redeemed',
        default=0,
        help_text='How often has this code been redeemed?'
    )

    @property
    def unused_credits(self):
        return self.credits_gained - self.credits_redeemed

    @property
    def no_free_transcations(self):
        return int(self.unused_credits / settings.NO_REFERRALS_REQUIRED)

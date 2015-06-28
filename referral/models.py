from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from referral.utils import generate_referral_code
from referral.exceptions import ReferralException


def create_referral_code(user):

    while True:
        code = generate_referral_code()

        try:
            Referral.objects.get(code__iexact=code)
        except Referral.DoesNotExist:
            break

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

    referred_by = models.ForeignKey(
        'self',
        null=True
    )

    referred_to = models.ManyToManyField(
        'self',
        null=True,
        symmetrical=False,
        related_name='referer'
    )

    code = models.CharField(
        'Referral code',
        max_length=50,
        unique=True,
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
        help_text='How many of the credits have been redeemed?'
    )

    @property
    def unused_credits(self):
        return self.credits_gained - self.credits_redeemed

    @property
    def no_free_transcations(self):
        return int(self.unused_credits / settings.REFERRALS_PER_TXN)

    @property
    def free_transaction(self):
        return self.no_free_transcations > 0

    def __unicode__(self):
        return '{}'.format(self.user.email)

    def redeem_transaction(self):
        if self.no_free_transcations < 1:
            raise ReferralException

        if self.credits_gained < settings.REFERRALS_PER_TXN:
            raise ReferralException

        self.credits_redeemed += settings.REFERRALS_PER_TXN
        self.save()

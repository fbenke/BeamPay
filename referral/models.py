from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from referral.utils import generate_referral_code
from referral.exceptions import ReferralException

from payment import constants


def create_referral_code(user, referral_code=None):

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

    if referral_code:
        try:
            referred_by = Referral.objects.get(code=referral_code)
            referral.referred_by = referred_by

        except Referral.DoesNotExist:
            pass

    referral.save()

    return referral


class Referral(models.Model):

    user = models.OneToOneField(
        User,
        unique=True,
        null=True,
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
    def free_transaction_no(self):
        return int(self.unused_credits / settings.REFERRALS_PER_TXN)

    @property
    def free_transaction(self):
        return self.free_transaction_no > 0

    def __unicode__(self):
        try:
            return '{}'.format(self.user.email)
        except AttributeError:
            return '{}'.format(self.code)

    def redeem_transaction(self):
        if self.free_transaction_no < 1:
            raise ReferralException(constants.REFERRAL_ERROR)

        if self.credits_gained < settings.REFERRALS_PER_TXN:
            raise ReferralException(constants.REFERRAL_ERROR)

        self.credits_redeemed += settings.REFERRALS_PER_TXN
        self.save()

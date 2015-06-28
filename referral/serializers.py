from rest_framework import serializers

from referral import models


class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Referral
        fields = ('referred', 'code', 'credits_gained',
                  'credits_redeemed', 'unused_credits',
                  'no_free_transcations')

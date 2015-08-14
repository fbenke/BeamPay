from rest_framework import serializers

from referral import models


class ReferralSerializer(serializers.ModelSerializer):

    referred_by = serializers.StringRelatedField()
    referred_to = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Referral
        fields = (
            'code', 'credits_gained', 'credits_redeemed',
            'unused_credits', 'free_transaction_no',
            'referred_to', 'referred_by'
        )

from rest_framework import serializers

from referral import models


class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Referral

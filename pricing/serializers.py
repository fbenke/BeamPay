from rest_framework import serializers

from pricing.models import ExchangeRate, ServiceFee


class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate
        fields = ['id', 'usd_ghs']


class ServiceFeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceFee
        fields = ['id', 'service', 'fixed_fee', 'percentual_fee']

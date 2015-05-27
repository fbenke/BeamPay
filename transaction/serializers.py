from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from beam_value.utils.exceptions import APIException

from transaction import models
from transaction import constants
from transaction.utils import generate_reference_number

from recipient.models import Recipient
from recipient.serializers import RecipientSerializer

from pricing.models import get_current_exchange_rate, get_current_airtime_fee

from account.models import BeamProfile


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        read_only_fields = ('timestamp', 'comment')
        fields = read_only_fields


class TransactionSerializer(serializers.ModelSerializer):

    recipient = RecipientSerializer(many=False)
    comments = CommentSerializer(many=True)

    class Meta:
        model = models.Transaction
        depth = 1
        read_only_fields = (
            'id', 'reference_number', 'state', 'last_changed', 'transaction_type',
            'additional_info', 'cost_of_delivery_usd', 'cost_of_delivery_ghs',
            'service_charge', 'recipient', 'comments'
        )
        fields = read_only_fields + ()


class CreateTransactionSerializer(serializers.ModelSerializer):

    recipient = RecipientSerializer(many=False, required=False)
    recipient_id = serializers.IntegerField(required=False)
    preferred_contact_method = serializers.CharField(required=False)

    class Meta:

        model = models.Transaction

        fields = (
            'recipient', 'recipient_id', 'preferred_contact_method',
            'transaction_type', 'additional_info'
        )

    def create(self, validated_data):

        user = validated_data.pop('user')

        if validated_data.get('preferred_contact_method', None):

            if validated_data.get('preferred_contact_method') not in BeamProfile.CONTACT_METHOD_CHOICES:
                raise APIException(constants.INVALID_PARAMETERS)

            user.profile.preferred_contact_method = validated_data.pop('preferred_contact_method')
            user.profile.save()

        exchange_rate = get_current_exchange_rate()

        if validated_data.get('recipient', None):
            recipient_data = validated_data.pop('recipient')
            recipient = Recipient.objects.create(user=user, **recipient_data)

        elif validated_data.get('recipient_id', None):

            try:
                recipient_id = validated_data.pop('recipient_id')
                recipient = Recipient.objects.get(user__id=user.id, id=recipient_id)

            except ObjectDoesNotExist:
                raise APIException(constants.INVALID_PARAMETERS)

        else:
            raise APIException(constants.INVALID_PARAMETERS)

        transaction = models.Transaction.objects.create(
            sender=user,
            recipient=recipient,
            exchange_rate=exchange_rate,
            **validated_data
        )

        transaction.reference_number = generate_reference_number()
        transaction.save()

        transaction.add_status_change('INIT')

        return transaction


class CreateAirtimeTopupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AirtimeTopup
        fields = ('phone_number', 'network', 'amount_ghs')

    def create(self, validated_data):

        user = validated_data.pop('user')

        exchange_rate = get_current_exchange_rate()
        airtime_fee = get_current_airtime_fee()

        airtime_topup = models.AirtimeTopup.objects.create(
            sender=user,
            exchange_rate=exchange_rate,
            service_fee=airtime_fee,
            **validated_data
        )

        airtime_topup.reference_number = generate_reference_number()
        print airtime_topup.reference_number
        airtime_topup.save()

        return airtime_topup

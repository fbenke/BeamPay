from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from beam_value.utils.exceptions import APIException

from transaction import models
from transaction import constants
from transaction.utils import generate_reference_number

from recipient.models import Recipient
from recipient.serializers import RecipientSerializer

from pricing.models import get_current_exchange_rate, get_current_airtime_fee

from account import constants as c


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        read_only_fields = ('timestamp', 'comment')
        fields = read_only_fields


class GenericTransactionSerializer(serializers.ModelSerializer):

    recipient = RecipientSerializer(many=False, required=False)
    recipient_id = serializers.IntegerField(required=False)

    def _get_recipient(self, validated_data, user):

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

        return recipient


class CreateValetSerializer(GenericTransactionSerializer):

    preferred_contact_method = serializers.CharField(required=False)

    class Meta:
        model = models.ValetTransaction
        fields = (
            'recipient', 'recipient_id', 'description',
            'preferred_contact_method'
        )

    def create(self, validated_data):

        user = validated_data.pop('user')

        recipient = self._get_recipient(validated_data, user)

        if validated_data.get('preferred_contact_method', None):

            if validated_data.get('preferred_contact_method') not in c.CONTACT_METHODS:
                raise APIException(constants.INVALID_PARAMETERS)

            user.profile.preferred_contact_method = validated_data.pop(
                'preferred_contact_method')
            user.profile.save()

        transaction = models.ValetTransaction.objects.create(
            sender=user,
            recipient=recipient,
            **validated_data
        )

        transaction.reference_number = generate_reference_number()
        transaction.save()
        transaction.add_status_change('INIT')

        return transaction


class CreateAirtimeTopupSerializer(GenericTransactionSerializer):

    class Meta:
        model = models.AirtimeTopup
        fields = ('recipient', 'recipient_id', 'network', 'amount_ghs')

    def create(self, validated_data):

        user = validated_data.pop('user')

        exchange_rate = get_current_exchange_rate()
        airtime_fee = get_current_airtime_fee()

        recipient = self._get_recipient(validated_data, user)

        airtime_topup = models.AirtimeTopup.objects.create(
            sender=user,
            exchange_rate=exchange_rate,
            airtime_service_fee=airtime_fee,
            recipient=recipient,
            service_charge=airtime_fee.fee,
            **validated_data
        )

        airtime_topup.reference_number = generate_reference_number()
        airtime_topup.amount_usd = airtime_topup.amount_ghs / exchange_rate.usd_ghs
        airtime_topup.save()
        airtime_topup.add_status_change('INIT')

        return airtime_topup


# class TransactionSerializer(serializers.ModelSerializer):

#     recipient = RecipientSerializer(many=False)
#     comments = CommentSerializer(many=True)

#     class Meta:
#         model = models.Transaction
#         depth = 1
#         read_only_fields = (
#             'id', 'reference_number', 'state', 'last_changed', 'transaction_type',
#             'additional_info', 'cost_of_delivery_usd', 'cost_of_delivery_ghs',
#             'service_charge', 'recipient', 'comments'
#         )
#         fields = read_only_fields + ()

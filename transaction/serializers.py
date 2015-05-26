from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from beam_value.utils.exceptions import APIException

from transaction import models
from transaction import constants

from recipient.models import Recipient
from recipient.serializers import RecipientSerializer

from pricing.models import get_current_exchange_rate


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

    class Meta:

        model = models.Transaction

        fields = (
            'recipient', 'recipient_id', 'transaction_type', 'additional_info'
        )

    def create(self, validated_data):

        user = validated_data.pop('user')
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

        transaction.generate_reference_number()
        transaction.save()

        return transaction

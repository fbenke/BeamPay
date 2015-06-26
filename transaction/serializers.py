from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from beam_value.utils.exceptions import APIException

from transaction import models
from transaction import constants
from transaction.utils import generate_reference_number

from recipient.models import Recipient
from recipient.serializers import RecipientSerializer

from pricing.models import get_current_exchange_rate, get_current_service_fee

from account import constants as c


common_serializer_fields = ('recipient', 'recipient_id', 'preferred_contact_method')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        read_only_fields = ('timestamp', 'comment')
        fields = read_only_fields


class GenericTransactionSerializer(serializers.ModelSerializer):

    recipient = RecipientSerializer(many=False, required=False)
    recipient_id = serializers.IntegerField(required=False)
    preferred_contact_method = serializers.CharField(required=False)

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

    def _update_contact_method(self, validated_data, user):

        if validated_data.get('preferred_contact_method', None):

            if validated_data.get('preferred_contact_method') not in c.CONTACT_METHODS:
                raise APIException(constants.INVALID_PARAMETERS)

            user.profile.preferred_contact_method = validated_data.pop(
                'preferred_contact_method')
            user.profile.save()

    def _initial_values(self, transaction):

        transaction.reference_number = generate_reference_number()
        transaction.save()
        transaction.add_status_change(c.INIT)

    def create(self, validated_data):

        user = validated_data.pop('user')
        recipient = self._get_recipient(validated_data, user)
        self._update_contact_method(validated_data, user)

        transaction = self.Meta.model.objects.create(
            sender=user,
            recipient=recipient,
            **validated_data
        )

        self._initial_values(transaction)

        return transaction


class InstantPaymentSerializer(GenericTransactionSerializer):

    def create(self, validated_data):

        user = validated_data.pop('user')
        recipient = self._get_recipient(validated_data, user)
        self._update_contact_method(validated_data, user)

        exchange_rate = get_current_exchange_rate()
        service_fee = get_current_service_fee()

        transaction = self.Meta.model.objects.create(
            sender=user,
            exchange_rate=exchange_rate,
            service_fee=service_fee,
            recipient=recipient,
            **validated_data
        )

        transaction.amount_usd = transaction.amount_ghs / \
            transaction.exchange_rate.usd_ghs

        transaction.service_charge = transaction.amount_usd * \
            transaction.service_fee.percentual_fee + transaction.service_fee.fixed_fee

        self._initial_values(transaction)

        return transaction


class CreateAirtimeTopupSerializer(InstantPaymentSerializer):

    class Meta:
        model = models.AirtimeTopup
        fields = common_serializer_fields + ('phone_number', 'network', 'amount_ghs')


class CreateBillPaymentSerializer(InstantPaymentSerializer):

    class Meta:
        model = models.BillPayment
        fields = common_serializer_fields + (
            'account_number', 'amount_ghs', 'bill_type', 'reference')


class CreateValetSerializer(GenericTransactionSerializer):

    class Meta:
        model = models.ValetTransaction
        fields = common_serializer_fields + ('description', )


class CreateSchoolFeeSerializer(GenericTransactionSerializer):

    class Meta:
        model = models.SchoolFeePayment
        fields = common_serializer_fields + (
            'ward_name', 'school', 'additional_info')


class CreateGiftOrderSerializer(GenericTransactionSerializer):

    class Meta:
        model = models.Gift
        fields = common_serializer_fields + (
            'gift_type', 'delivery_address', 'delivery_time', 'additional_info')


class TransactionSerializer(serializers.Serializer):
    txn_type = serializers.CharField(max_length=20)
    data = serializers.CharField(max_length=10000)


class AirtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirtimeTopup


class BillPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillPayment


class SchoolFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolFeePayment


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gift


class ValetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ValetTransaction

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from beam_value.utils.exceptions import APIException

from transaction import models
from transaction import constants
from transaction.utils import generate_reference_number, round_amount

from recipient.models import Recipient
from recipient.serializers import RecipientSerializer

from pricing.models import get_current_exchange_rate, get_current_service_fee

from account import constants as c
from transaction import constants as t


common_serializer_fields = (
    'recipient', 'recipient_id', 'preferred_contact_method',
    'preferred_contact_details', 'amount_ghs'
)


class ViewCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        read_only_fields = ('author', 'timestamp', 'comment')
        fields = read_only_fields


class GenericCreateTransactionSerializer(serializers.ModelSerializer):

    recipient = RecipientSerializer(many=False, required=False)
    recipient_id = serializers.IntegerField(required=False)
    preferred_contact_method = serializers.CharField(required=False)
    preferred_contact_details = serializers.CharField(required=False)

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

        try:
            contact_method = validated_data.pop('preferred_contact_method')
        except KeyError:
            contact_method = None

        try:
            contact_details = validated_data.pop('preferred_contact_details')
        except KeyError:
            contact_details = None

        if contact_method and contact_details:

            if contact_method not in c.CONTACT_METHODS:
                raise APIException(constants.INVALID_PARAMETERS)

            user.profile.preferred_contact_method = contact_method
            user.profile.preferred_contact_details = contact_details

            user.profile.save()

    def _initial_values(self, transaction):

        transaction.reference_number = generate_reference_number()
        transaction.save()
        transaction.add_status_change(t.INIT)

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


class CreateInstantPaymentSerializer(GenericCreateTransactionSerializer):

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

        transaction.amount_usd = round_amount(
            transaction.amount_ghs / transaction.exchange_rate.usd_ghs)

        transaction.service_charge = round_amount(
            transaction.amount_usd * transaction.service_fee.percentual_fee +
            transaction.service_fee.fixed_fee)

        self._initial_values(transaction)

        return transaction


class CreateAirtimeTopupSerializer(CreateInstantPaymentSerializer):

    class Meta:
        model = models.AirtimeTopup
        fields = common_serializer_fields + ('phone_number', 'network')


class CreateBillPaymentSerializer(CreateInstantPaymentSerializer):

    class Meta:
        model = models.BillPayment
        fields = common_serializer_fields + (
            'account_number', 'bill_type', 'reference')


class CreateValetSerializer(GenericCreateTransactionSerializer):

    class Meta:
        model = models.ValetTransaction
        fields = common_serializer_fields + ('description', )


class CreateSchoolFeeSerializer(GenericCreateTransactionSerializer):

    class Meta:
        model = models.SchoolFeePayment
        fields = common_serializer_fields + (
            'ward_name', 'school', 'additional_info')


class CreateGiftOrderSerializer(GenericCreateTransactionSerializer):

    class Meta:
        model = models.Gift
        fields = common_serializer_fields + (
            'gift_type', 'delivery_address', 'delivery_time', 'additional_info')


class GenericListItemSerializer(serializers.Serializer):
    transaction_type = serializers.CharField(max_length=20)
    data = serializers.CharField(max_length=10000)


class ViewAirtimeSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(many=False)
    total_charge_usd = serializers.FloatField()

    class Meta:
        model = models.AirtimeTopup


class ViewBillPaymentSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(many=False)
    total_charge_usd = serializers.FloatField()

    class Meta:
        model = models.BillPayment


class ViewSchoolFeeSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(many=False)
    total_charge_usd = serializers.FloatField()

    class Meta:
        model = models.SchoolFeePayment


class ViewGiftSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(many=False)
    total_charge_usd = serializers.FloatField()

    class Meta:
        model = models.Gift


class ViewValetSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(many=False)
    total_charge_usd = serializers.FloatField()

    class Meta:
        model = models.ValetTransaction

from itertools import chain

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.generics import (
    GenericAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin
from beam_value.utils.ip_analysis import country_blocked, is_tor_node,\
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
from beam_value.utils.exceptions import APIException

from account.utils import AccountException

from pricing.models import get_current_exchange_rate, get_current_service_fees

from transaction import serializers
from transaction import constants
from pricing import constants as p
from transaction import models
from referral.models import create_referral_code
from account.serializers import ProfileSerializer
from referral.serializers import ReferralSerializer
from pricing.serializers import ExchangeRateSerializer, ServiceFeeSerializer


mod = __import__('transaction.models', fromlist=constants.TRANSACTION_MODELS)


class CreateGenericTransaction(GenericAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request):

        # block countries we are not licensed to operate in and tor clients
        if country_blocked(request) or is_tor_node(request):
            return Response(status=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        serializer = self.serializer_class(data=request.data)

        try:

            self.check_parameters(request)

            if serializer.is_valid():

                transaction = serializer.save(user=request.user)

                self.post_created(transaction)

                return Response(
                    self.generate_response(transaction),
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (AccountException, APIException) as e:

            return Response(
                {'detail': e[0]},
                status=status.HTTP_400_BAD_REQUEST
            )

    def check_parameters(self, request):

        # check if basic profile information incomplete
        if not request.user.profile.information_complete:
            raise AccountException(constants.PROFILE_INCOMPLETE)

    def generate_response(self, transaction):

        return {
            'transaction_id': transaction.id,
            'reference_number': transaction.reference_number
        }

    def post_created(self, transaction):
        pass


class CreateTransactionRequest(CreateGenericTransaction):

    def post_created(self, transaction):
        transaction.post_created()


class CreateInstantPayment(CreateGenericTransaction):

    def generate_response(self, transaction):

        response_dict = super(CreateInstantPayment, self).generate_response(
            transaction)
        response_dict['charge_usd'] = transaction.total_charge_usd
        return response_dict


class CreateAirtimeTopup(CreateInstantPayment):

    serializer_class = serializers.CreateAirtimeTopupSerializer

    def check_parameters(self, request):

        super(CreateInstantPayment, self).check_parameters(request)

        amount_ghs = request.data.get('amount_ghs', None)
        exchange_rate_id = request.data.get('exchange_rate_id', None)
        service_fee_id = request.data.get('service_fee_id', None)

        if not amount_ghs or not exchange_rate_id or not service_fee_id:
            raise APIException(constants.INVALID_PARAMETERS)

        # check if Exchange Rate or Service Charge has expired
        service_fees = get_current_service_fees()
        service_fee = None

        for fee in service_fees:
            if fee.service == p.AIRTIME:
                service_fee = fee
                break

        if (get_current_exchange_rate().id != exchange_rate_id or
                service_fee.id != service_fee_id):
            raise APIException(constants.PRICING_EXPIRED)


class CreateBillPayment(CreateInstantPayment):

    serializer_class = serializers.CreateBillPaymentSerializer

    def check_parameters(self, request):

        super(CreateInstantPayment, self).check_parameters(request)

        amount_ghs = request.data.get('amount_ghs', None)
        exchange_rate_id = request.data.get('exchange_rate_id', None)
        service_fee_id = request.data.get('service_fee_id', None)

        if not amount_ghs or not exchange_rate_id or not service_fee_id:
            raise APIException(constants.INVALID_PARAMETERS)

        # check if Exchange Rate or Service Charge has expired
        service_fees = get_current_service_fees()
        service_fee = None

        for fee in service_fees:
            if fee.service == p.BILL:
                service_fee = fee
                break

        if (get_current_exchange_rate().id != exchange_rate_id or
                service_fee.id != service_fee_id):
            raise APIException(constants.PRICING_EXPIRED)


class CreateValetTransaction(CreateTransactionRequest):

    serializer_class = serializers.CreateValetSerializer


class CreateSchoolFeePayment(CreateTransactionRequest):

    serializer_class = serializers.CreateSchoolFeeSerializer


class CreateGiftOrder(CreateTransactionRequest):

    serializer_class = serializers.CreateGiftOrderSerializer


MODEL_2_SERIALIZER = {
    models.AirtimeTopup: serializers.ViewAirtimeSerializer,
    models.BillPayment: serializers.ViewBillPaymentSerializer,
    models.SchoolFeePayment: serializers.ViewSchoolFeeSerializer,
    models.Gift: serializers.ViewGiftSerializer,
    models.ValetTransaction: serializers.ViewValetSerializer
}


class ViewTransactions(ListAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)
    serializer_class = serializers.GenericListItemSerializer
    paginate_by = 20

    def get(self, request, *args, **kwargs):

        states = list(
            set(constants.TRANSACTION_STATES) - set((constants.INIT,)))
        user = self.request.user
        airtime = models.AirtimeTopup.objects.filter(
            sender=user, state__in=states)
        bills = models.BillPayment.objects.filter(
            sender=user, state__in=states)
        school_fees = models.SchoolFeePayment.objects.filter(sender=user)
        gifts = models.Gift.objects.filter(sender=user)
        valet = models.ValetTransaction.objects.filter(sender=user)

        results_list = list(chain(
            airtime, bills, school_fees, valet, gifts)
        )

        sorted_list = sorted(
            results_list, key=lambda instance: instance.last_changed,
            reverse=True)

        results = list()

        for entry in sorted_list:

            item_type = entry.__class__.__name__.lower()
            serializer_class = MODEL_2_SERIALIZER[entry.__class__]
            serializer = serializer_class(entry)

            results.append(
                {'transaction_type': item_type, 'data': serializer.data})

        return Response(results)


class GetTransaction(RetrieveAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def get(self, request, *args, **kwargs):

        user = self.request.user
        txn_type = request.query_params.get('type', None)

        try:

            txn_class = getattr(mod, constants.TXN_TYPE_2_MODEL[txn_type])

            transaction = txn_class.objects.get(
                sender=user,
                pk=self.kwargs['pk']
            )

            serializer_class = MODEL_2_SERIALIZER[txn_class]
            serializer = serializer_class(transaction)

            transaction_data = serializer.data

            # gater and deserialize comments
            comments = models.Comment.objects.filter(
                content_type__model=constants.TXN_TYPE_2_MODEL[txn_type].lower(),
                object_id=transaction.id
            )

            serializer_class = serializers.ViewCommentSerializer
            comment_data = []

            for c in comments:
                serializer = serializer_class(c)
                comment_data.append(serializer.data)

            transaction_data['comments'] = comment_data

            return Response(transaction_data)

        except (ObjectDoesNotExist, KeyError):

            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )


class InstaPaySetupView(RetrieveAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def get(self, request, *args, **kwargs):

        profile = self.request.user.profile
        referral = None
        exchange_rate = {}
        airtime_service_fee = None
        bill_service_fee = None

        try:
            referral = self.request.user.referral
        except ObjectDoesNotExist:
            referral = create_referral_code(self.request.user)

        try:
            exchange_rate = get_current_exchange_rate()
            service_fees = get_current_service_fees()

            if service_fees[0].service == p.AIRTIME:
                airtime_service_fee = service_fees[0]
                bill_service_fee = service_fees[1]
            else:
                airtime_service_fee = service_fees[1]
                bill_service_fee = service_fees[0]

        except Exception:
            exchange_rate = {}
            airtime_service_fee = None
            bill_service_fee = None

        insta_pay = {}
        insta_pay['profile'] = ProfileSerializer(profile).data

        if exchange_rate:
            insta_pay['pricing'] = ExchangeRateSerializer(
                exchange_rate).data
            insta_pay['pricing']['exchange_rate_id'] = insta_pay['pricing']['id']
            insta_pay['pricing']['airtime'] = ServiceFeeSerializer(
                airtime_service_fee).data
            insta_pay['pricing']['bill'] = ServiceFeeSerializer(
                bill_service_fee).data

        insta_pay['referral'] = ReferralSerializer(referral).data

        return Response(insta_pay)

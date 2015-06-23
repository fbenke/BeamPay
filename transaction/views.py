from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin
from beam_value.utils.ip_analysis import country_blocked, is_tor_node,\
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
from beam_value.utils.exceptions import APIException

from account.utils import AccountException

from pricing.models import get_current_exchange_rate, get_current_service_fee

from transaction import serializers
from transaction import constants


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

                return Response(
                    self.generate_response(transaction),
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return {'reference_number': transaction.reference_number}


class CreateAirtimeTopup(CreateGenericTransaction):

    serializer_class = serializers.CreateAirtimeTopupSerializer

    def check_parameters(self, request):

        super(CreateAirtimeTopup, self).check_parameters(request)

        # check if Exchange Rate or Airtime Fee has expired
        exchange_rate_id = request.data.get('exchange_rate_id', None)
        service_fee_id = request.data.get('service_fee_id', None)

        if not exchange_rate_id or not service_fee_id:
            raise APIException(constants.INVALID_PARAMETERS)

        if (get_current_exchange_rate().id != exchange_rate_id or
                get_current_service_fee().id != service_fee_id):
            raise APIException(constants.PRICING_EXPIRED)

    def generate_response(self, transaction):

        response_dict = super(CreateAirtimeTopup, self).generate_response(transaction)
        response_dict['charge_usd'] = transaction.total_charge_usd
        return response_dict


class CreateValetTransaction(CreateGenericTransaction):

    serializer_class = serializers.CreateValetSerializer


class CreateSchoolFeePayment(CreateGenericTransaction):

    serializer_class = serializers.CreateSchoolFeeSerializer


class CreateBillPayment(CreateGenericTransaction):

    serializer_class = serializers.CreateBillPaymentSerializer


class CreateGiftOrder(CreateGenericTransaction):

    serializer_class = serializers.CreateGiftOrderSerializer

# class ViewTransactions(ListAPIView):

#     serializer_class = serializers.TransactionSerializer
#     permission_classes = (IsAuthenticated, IsNoAdmin)

#     paginate_by = 10

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Transaction.objects.filter(sender__id=user.id)
#         return queryset


# class GetTransaction(RetrieveAPIView):

#     serializer_class = serializers.TransactionSerializer
#     permission_classes = (IsAuthenticated, IsNoAdmin)

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Transaction.objects.filter(sender__id=user.id)
#         return queryset

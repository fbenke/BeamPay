from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin
from beam_value.utils.ip_analysis import country_blocked, is_tor_node,\
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
from beam_value.utils.exceptions import APIException

from transaction import serializers
from transaction import constants

from pricing.models import get_current_exchange_rate, get_current_airtime_fee


# class CreateTransaction(GenericAPIView):

#     serializer_class = serializers.CreateTransactionSerializer
#     permission_classes = (IsAuthenticated, IsNoAdmin)

#     def post(self, request):

#         # block countries we are not licensed to operate in and tor clients
#         if country_blocked(request) or is_tor_node(request):
#             return Response(status=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

#         serializer = self.serializer_class(data=request.data)

#         # check if Exchange Rate has expired
#         exchange_rate_id = request.data.get('exchange_rate_id', None)

#         if not exchange_rate_id:
#             return Response(
#                 {'detail': constants.INVALID_PARAMETERS},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if get_current_exchange_rate().id != exchange_rate_id:
#             return Response(
#                 {'detail': constants.PRICING_EXPIRED},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             if serializer.is_valid():

#                 # basic profile information incomplete
#                 if not request.user.profile.information_complete:
#                     return Response(
#                         {'detail': constants.PROFILE_INCOMPLETE},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#                 transaction = serializer.save(user=request.user)

#                 return Response(
#                     {'reference_number': transaction.reference_number},
#                     status=status.HTTP_201_CREATED)

#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except APIException as e:

#             return Response(
#                 {'detail': e[0]}, status=status.HTTP_400_BAD_REQUEST)


class CreateAirtimeTopup(GenericAPIView):

    serializer_class = serializers.CreateAirtimeTopupSerializer
    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request):

        # block countries we are not licensed to operate in and tor clients
        if country_blocked(request) or is_tor_node(request):
            return Response(status=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        serializer = self.serializer_class(data=request.data)

        # check if Exchange Rate or Airtime Fee has expired
        exchange_rate_id = request.data.get('exchange_rate_id', None)
        airtime_fee_id = request.data.get('airtime_fee_id', None)

        if not exchange_rate_id or not airtime_fee_id:
            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (get_current_exchange_rate().id != exchange_rate_id or
                get_current_airtime_fee().id != airtime_fee_id):
            return Response(
                {'detail': constants.PRICING_EXPIRED},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:

            if serializer.is_valid():

                # basic profile information incomplete
                if not request.user.profile.information_complete:
                    return Response(
                        {'detail': constants.PROFILE_INCOMPLETE},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                airtime_topup = serializer.save(user=request.user)

                return Response(
                    {'reference_number': airtime_topup.reference_number,
                     'charge_usd': airtime_topup.total_charge_usd},
                    status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:

            return Response(
                {'detail': e[0]}, status=status.HTTP_400_BAD_REQUEST)


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

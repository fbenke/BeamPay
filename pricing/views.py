from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pricing.models import get_current_exchange_rate, get_current_airtime_fee


class PricingCurrent(APIView):

    def get(self, request, *args, **kwargs):

        response_dict = {}

        try:
            exchange_rate = get_current_exchange_rate()
            response_dict['exchange_rate_id'] = exchange_rate.id
            response_dict['usd_ghs'] = exchange_rate.usd_ghs

            airtime_fee = get_current_airtime_fee()
            response_dict['airtime_fee_id'] = airtime_fee.id
            response_dict['airtime_fee'] = airtime_fee.fee

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_dict)

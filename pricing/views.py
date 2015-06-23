from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pricing.models import get_current_exchange_rate, get_current_service_fee


class PricingCurrent(APIView):

    def get(self, request, *args, **kwargs):

        response_dict = {}

        try:
            exchange_rate = get_current_exchange_rate()
            response_dict['exchange_rate_id'] = exchange_rate.id
            response_dict['usd_ghs'] = exchange_rate.usd_ghs

            service_fee = get_current_service_fee()
            response_dict['service_fee_id'] = service_fee.id
            response_dict['fixed_fee'] = service_fee.fixed_fee
            response_dict['percentual_fee'] = service_fee.percentual_fee

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_dict)

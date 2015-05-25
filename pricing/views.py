from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pricing.models import get_current_exchange_rate


class PricingCurrent(APIView):

    def get(self, request, *args, **kwargs):

        response_dict = {}

        try:
            exchange_rate = get_current_exchange_rate()
            response_dict['id'] = exchange_rate.id
            response_dict['usd_ghs'] = exchange_rate.usd_ghs

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_dict)

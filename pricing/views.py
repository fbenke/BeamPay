from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pricing.models import get_current_exchange_rate, get_current_service_fees
from pricing.constants import AIRTIME, BILL


class PricingCurrent(APIView):

    def get(self, request, *args, **kwargs):

        response_dict = {}

        try:
            exchange_rate = get_current_exchange_rate()
            response_dict['exchange_rate_id'] = exchange_rate.id
            response_dict['usd_ghs'] = exchange_rate.usd_ghs

            service_fees = get_current_service_fees()
            response_dict['service_fees'] = {}

            for service_fee in service_fees:
                if service_fee.service == AIRTIME:
                    response_dict['airtime']['service_fee_id'] = service_fee.id
                    response_dict['airtime']['fixed_fee'] = service_fee.fixed_fee
                    response_dict['airtime']['percentual_fee'] = service_fee.percentual_fee
                elif service_fee.service == BILL:
                    response_dict['bill']['service_fee_id'] = service_fee.id
                    response_dict['bill']['fixed_fee'] = service_fee.fixed_fee
                    response_dict['bill']['percentual_fee'] = service_fee.percentual_fee

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response_dict)

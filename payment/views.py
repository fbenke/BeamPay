import stripe
from stripe import Charge
from stripe.error import CardError, InvalidRequestError

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin

from transaction.models import Transaction, AirtimeTopup
from transaction.utils import TransactionException

from payment import constants


class StripeChargeTransaction(GenericAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request):

        token = request.data.get('stripe_token', None)
        transaction_id = request.data.get('transaction_id', None)

        if not token or not transaction_id:
            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            user_id = request.user.id

            transaction = Transaction.objects.get(
                id=transaction_id,
                sender__id=user_id)

            if transaction.charge_usd:
                amount_usd = int(transaction.charge_usd * 100)
            else:
                raise TransactionException

            stripe.api_key = settings.STRIPE_SECRET_KEY

            charge = Charge.create(
                amount=amount_usd,
                currency='USD',
                source=token,
                description=transaction.reference_number
            )

            transaction.payment_reference = charge.id
            transaction.payment_processor = Transaction.STRIPE
            transaction.state = Transaction.PAID
            transaction.save()

            transaction.add_status_change(comment=Transaction.PAID)

            return Response(status=status.HTTP_201_CREATED)

        except (CardError, InvalidRequestError) as e:
            return Response(
                {'detail': e[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except (ObjectDoesNotExist, TransactionException):
            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )


class StripeChargeAirtime(GenericAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request):

        token = request.data.get('stripe_token', None)
        transaction_id = request.data.get('transaction_id', None)

        if not token or not transaction_id:
            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            user_id = request.user.id

            airtime_topup = AirtimeTopup.objects.get(
                id=transaction_id,
                sender__id=user_id)

            if airtime_topup.charge_usd:
                amount_usd = int(airtime_topup.charge_usd * 100)
            else:
                raise TransactionException

            stripe.api_key = settings.STRIPE_SECRET_KEY

            charge = Charge.create(
                amount=amount_usd,
                currency='USD',
                source=token,
                description=airtime_topup.reference_number
            )

            airtime_topup.payment_reference = charge.id
            airtime_topup.payment_processor = AirtimeTopup.STRIPE
            airtime_topup.state = AirtimeTopup.PAID
            airtime_topup.paid_at = timezone.now()
            airtime_topup.save()

            airtime_topup.post_paid()

            return Response(status=status.HTTP_201_CREATED)

        except (CardError, InvalidRequestError) as e:
            return Response(
                {'detail': e[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except (ObjectDoesNotExist, TransactionException):
            return Response(
                {'detail': constants.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

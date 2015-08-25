import stripe
from stripe import Charge
from stripe.error import CardError, InvalidRequestError

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin

from transaction.utils import TransactionException
from transaction import constants as t

from payment import constants as p

from referral.exceptions import ReferralException

mod = __import__('transaction.models', fromlist=t.INSTANT_PAYMENT_MODELS)


class StripeCharge(GenericAPIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request, *args, **kwargs):

        try:

            token = request.data.get('stripe_token', None)
            transaction_id = request.data.get('transaction_id', None)
            txn_type = request.data.get('type', None)

            if not token or not transaction_id:
                raise TransactionException

            if not txn_type or txn_type not in t.INSTANT_PAYMENTS:
                raise TransactionException

            payment_class = getattr(mod, t.TXN_TYPE_2_MODEL[txn_type])

            user_id = request.user.id

            transaction = payment_class.objects.get(
                id=transaction_id,
                sender__id=user_id,
                state=t.INIT
            )

            # redeem free transaction
            referral = request.user.referral

            if referral.free_transaction:
                transaction.service_charge = 0
                transaction.free_from_referral = True

            amount_usd = int(transaction.total_charge_usd * 100)

            stripe.api_key = settings.STRIPE_SECRET_KEY

            charge = Charge.create(
                amount=amount_usd,
                currency='USD',
                source=token,
                description=transaction.reference_number
            )

            transaction.payment_reference = charge.id
            transaction.payment_processor = t.STRIPE
            transaction.state = t.PAID
            transaction.save()
            transaction.add_status_change(t.PAID)
            transaction.post_paid()
            referral.redeem_transaction()

            return Response(status=status.HTTP_201_CREATED)

        except (InvalidRequestError, TypeError, ReferralException) as e:

            return Response(
                {'detail': e[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except CardError as e:

            transaction.payment_processor = t.STRIPE
            transaction.state = t.INVALID
            transaction.save()
            transaction.add_status_change(t.INVALID)

            return Response(
                {'detail': p.STRIPE_ERROR,
                 'message': e[0]},
                status=status.HTTP_400_BAD_REQUEST
            )

        except (ObjectDoesNotExist, TransactionException):

            return Response(
                {'detail': p.INVALID_PARAMETERS},
                status=status.HTTP_400_BAD_REQUEST
            )

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from beam_value.permissions import IsNoAdmin
from beam_value.utils.exceptions import APIException

from referral import constants
from referral import serializers
from referral.models import Referral, create_referral_code


class ViewReferral(APIView):

    serializer_class = serializers.ReferralSerializer
    permission_classes = (IsAuthenticated, IsNoAdmin)

    def get(self, request):
        referral = None
        try:
            user = self.request.user
            referral = Referral.objects.get(user=user)
        except ObjectDoesNotExist:
            referral = create_referral_code(self.request.user)

        serializer = self.serializer_class(referral)
        return Response(serializer.data)


class ReferralStatus(APIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def get(self, request):
        referral = None
        try:
            user = self.request.user
            referral = Referral.objects.get(user=user)
        except ObjectDoesNotExist:
            referral = create_referral_code(self.request.user)

        return Response(
            {'free_transaction': referral.free_transaction}
        )


class AddReferral(APIView):

    permission_classes = (IsAuthenticated, IsNoAdmin)

    def post(self, request):

        user = self.request.user

        try:

            referer_code = request.data.get('code', None)

            if not referer_code:
                raise APIException(constants.INVALID_PARAMETERS)

            user_referral = Referral.objects.get(user=user)
            referred_by = Referral.objects.get(code=referer_code)

            if user_referral.referred_by:
                raise APIException(constants.CODE_USED_ALREADY)

            user_referral.referred_by = referred_by
            user_referral.credits_gained = settings.REFERRALS_PER_TXN
            user_referral.save()

            referred_by.referred_to.add(user_referral)
            referred_by.credits_gained = referred_by.credits_gained + 1
            referred_by.save()

            return Response()

        except ObjectDoesNotExist:

            return Response(
                {'detail': constants.INVALID_CODE},
                status=status.HTTP_400_BAD_REQUEST
            )

        except APIException as e:

            return Response(
                {'detail': e[0]},
                status=status.HTTP_400_BAD_REQUEST
            )

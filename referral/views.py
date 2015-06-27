from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beam_value.permissions import IsNoAdmin

from referral import serializers
from referral.models import Referral


class ViewReferral(RetrieveAPIView):

    serializer_class = serializers.ReferralSerializer
    permission_classes = (IsAuthenticated, IsNoAdmin)

    def get(self, request, *args, **kwargs):

        user = self.request.user
        referral = Referral.objects.get(user=user)
        serializer = self.serializer_class(referral)

        return Response(serializer.data)

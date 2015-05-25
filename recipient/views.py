from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from beam_value.permissions import IsNoAdmin

from recipient import serializers
from recipient.models import Recipient


class ViewRecipients(ListAPIView):

    serializer_class = serializers.RecipientSerializer
    permission_classes = (IsAuthenticated, IsNoAdmin)

    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Recipient.objects.filter(user__id=user.id)
        return queryset

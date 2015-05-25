from rest_framework import serializers

from recipient import models


class RecipientSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Recipient
        read_only_fields = ()
        read_and_write_fields = (
            'id', 'first_name', 'last_name', 'phone_number',
            'email', 'date_of_birth', 'relation'
        )

        fields = read_only_fields + read_and_write_fields

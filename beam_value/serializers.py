from rest_framework import serializers


class ShareEmailSerializer(serializers.Serializer):

    from_name = serializers.CharField()
    to_name = serializers.CharField()
    from_email = serializers.EmailField()
    to_email = serializers.EmailField()

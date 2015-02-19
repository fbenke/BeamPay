from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account import serializers

from beam_value.utils.ip_analysis import country_blocked, is_tor_node,\
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS


def send_activation_email(user, request, activation_key=None):

    if not activation_key:
        activation_key = user.userena_signup.activation_key

    context = {
        'user': user,
        'protocol': settings.PROTOCOL,
        'activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
        'activation_link': settings.MAIL_ACTIVATION_URL.format(activation_key),
        'site': get_site_by_request(request)
    }

    mails.send_mail(
        subject_template_name=settings.MAIL_ACTIVATION_SUBJECT,
        email_template_name=settings.MAIL_ACTIVATION_TEXT,
        html_email_template_name=settings.MAIL_ACTIVATION_HTML,
        to_email=user.email,
        from_email=settings.BEAM_MAIL_ADDRESS,
        context=context
    )


class Signup(APIView):

    serializer_class = serializers.SignupSerializer

    def post(self, request):

        # block countries we are not licensed to operate in and tor clients
        if country_blocked(request) or is_tor_node(request):
            return Response(status=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():

            user = serializer.save()

            if user:
                # store site the user signed up at
                user.profile.save()

                send_activation_email(user, request)

                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

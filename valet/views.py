from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from beam_value.utils import mails
from valet import constants


@api_view(['GET', 'POST'])
def add_whatsapp_number(request):
    number = request.data.get('number')
    if number and len(number) >= 10 and len(number) <= 13:

        mails.send_mail(
            subject_template_name=settings.MAIL_NOTIFY_ADMIN_VALET_SUBJECT,
            email_template_name=settings.MAIL_NOTIFY_ADMIN_VALET_TEXT,
            context={
                'number': number,
                'domain': settings.ENV_SITE_MAPPING[settings.ENV][settings.SITE_API]
            },
            to_email=mails.get_admin_mail_addresses()
        )

        return Response(
            {'success': 'message sent'}, status=status.HTTP_200_OK)

    else:
        return Response(
            {'detail': constants.INVALID_NUMBER},
            status=status.HTTP_400_BAD_REQUEST)

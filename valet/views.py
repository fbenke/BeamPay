# import xml.etree.ElementTree as ET
# import requests
# import unicodedata
# from operator import itemgetter
# from time import strptime

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from beam_value.utils import mails
from valet import constants
from valet.models import WhatsappRequest


@api_view(['GET', 'POST'])
def add_whatsapp_number(request):
    number = request.data.get('number')
    xmas = request.data.get('xmas', None)
    # email = request.data.get('email')

    if number and len(number) >= 10 and len(number) <= 13:
        wap_request, created = WhatsappRequest.objects.get_or_create(
            wap_number=number)

        mails.send_mail(
            subject_template_name=(
                settings.MAIL_NOTIFY_ADMIN_XMAS_SUBJECT if xmas else (
                    settings.MAIL_NOTIFY_ADMIN_VALET_SUBJECT)
            ),
            email_template_name=(
                settings.MAIL_NOTIFY_ADMIN_XMAS_TEXT if xmas else (
                    settings.MAIL_NOTIFY_ADMIN_VALET_TEXT)
            ),
            context={
                'number': number,
                'domain': settings.ENV_SITE_MAPPING[settings.ENV][
                    settings.SITE_API],
                'wap_request_id': wap_request.id,
                'protocol': settings.PROTOCOL,
                'created': created
            },
            to_email=mails.get_admin_mail_addresses()
        )

        # r = requests.get('https://medium.com/feed/beam-blog')
        # xml_data = ET.fromstring(
        #     unicodedata.normalize('NFKD', r.text).encode('ascii', 'ignore'))

        return Response(
            {'success': 'The number has been found successfully'},
            status=status.HTTP_200_OK)

    else:
        return Response(
            {'detail': constants.INVALID_NUMBER},
            status=status.HTTP_400_BAD_REQUEST)


def get_blogs_from_xml(xml_data):
    blogs = []

    for x in xrange(8, 11):
        blogs.append(xml_data[0][x][1].text)

    return blogs

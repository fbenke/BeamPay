from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from beam_value.utils.json_response import JSONResponse
from beam_value.utils import mails
from beam_value.serializers import ShareEmailSerializer


def page_not_found(request):
    return JSONResponse({'detail': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


def custom_error(request):
    return JSONResponse({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def permission_denied(request):
    return JSONResponse({'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)


def bad_request(request):
    return JSONResponse({'detail': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class ShareViaEmailView(APIView):

    serializer_class = ShareEmailSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            mails.send_mail(
                subject_template_name=settings.MAIL_SHARE_SUBJECT,
                email_template_name=settings.MAIL_SHARE_TEXT,
                html_email_template_name=settings.MAIL_SHARE_HTML,
                to_email=request.data.get('to_email'),
                from_email='{} <{}>'.format(
                    request.data.get('from_name'), request.data.get('from_email')),
                context={'first_name': request.data.get('to_name')}
            )

            return Response()

        else:
            return Response(serializer.errors)

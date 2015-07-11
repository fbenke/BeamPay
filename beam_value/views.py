from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from beam_value.utils.json_response import JSONResponse
from beam_value.utils import mails


def page_not_found(request):
    return JSONResponse({'detail': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)


def custom_error(request):
    return JSONResponse({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def permission_denied(request):
    return JSONResponse({'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)


def bad_request(request):
    return JSONResponse({'detail': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class ShareViaEmailView(APIView):

    def post(self, request):

        from_name = request.data.get('from_name', None)
        from_email = request.data.get('from_email', None)
        to_name = request.data.get('to_name', None)
        to_email = request.data.get('to_email', None)

        if (from_name and from_email and to_name and to_email):

            mails.send_mail(
                subject_template_name=settings.MAIL_SHARE_SUBJECT,
                email_template_name=settings.MAIL_SHARE_TEXT,
                html_email_template_name=settings.MAIL_SHARE_HTML,
                to_email=to_email,
                from_email='{} <{}>'.format(from_name, from_email),
                context={'first_name': to_name}
            )

            return Response()

        else:
            return Response({'detail': '0'})

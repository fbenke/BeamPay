from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from userena.models import UserenaSignup
from userena.utils import generate_sha1, get_datetime_now

from account import serializers
from account import constants
from account.utils import AccountException

from beam_value.utils import mails
from beam_value.utils.log import log_error

from beam_value.utils.ip_analysis import country_blocked, is_tor_node,\
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

from social.apps.django_app.utils import psa


def send_activation_email(user, activation_key=None):

    if not activation_key:
        activation_key = user.userena_signup.activation_key

    activation_url = settings.USER_BASE_URL +\
        settings.MAIL_ACTIVATION_URL.format(activation_key)

    mails.send_mail(
        subject_template_name=settings.MAIL_ACTIVATION_SUBJECT,
        email_template_name=settings.MAIL_ACTIVATION_TEXT,
        html_email_template_name=settings.MAIL_ACTIVATION_HTML,
        to_email=user.email,
        context={'activation_url': activation_url}
    )


def reissue_activation(activation_key):
    '''
    Rewritten version of UserenaSignup.objects.reissue_activation()
    to customize the sent email
    '''

    try:
        userena = UserenaSignup.objects.get(activation_key=activation_key)
    except UserenaSignup.objects.model.DoesNotExist:
        return None
    try:
        salt, new_activation_key = generate_sha1(userena.user.username)
        userena.activation_key = new_activation_key
        userena.save(using=UserenaSignup.objects._db)
        userena.user.date_joined = get_datetime_now()
        userena.user.save(using=UserenaSignup.objects._db)
        return new_activation_key
    except Exception:
        return None


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

                send_activation_email(user)

                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activation(APIView):

    def get(self, request, *args, **kwargs):

        activation_key = kwargs['activation_key']

        try:
            if not UserenaSignup.objects.check_expired_activation(activation_key):

                user = UserenaSignup.objects.activate_user(activation_key)

                # account successfully activated
                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'id': user.id}, status.HTTP_200_OK)

                else:
                    log_error(
                        'ERROR - User for activation key {} could not be found'.
                        format(activation_key)
                    )
                    return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

            # activation key expired
            else:
                return Response(
                    {'activation_key': activation_key, 'detail': constants.ACTIVATION_KEY_EXPIRED},
                    status.HTTP_400_BAD_REQUEST
                )
        # invalid key
        except UserenaSignup.DoesNotExist:
            return Response({'detail': constants.ACTIVATION_KEY_INVALID}, status.HTTP_400_BAD_REQUEST)


class ActivationRetry(APIView):

    def get(self, request, *args, **kwargs):

        activation_key = kwargs['activation_key']

        try:
            if UserenaSignup.objects.check_expired_activation(activation_key):

                user = UserenaSignup.objects.get(activation_key=activation_key).user

                new_activation_key = reissue_activation(activation_key)

                if new_activation_key:

                    send_activation_email(user, new_activation_key)

                    return Response({'email': user.email}, status=status.HTTP_201_CREATED)

                else:
                    log_error(
                        'ERROR - activation key could not be generated for expired key {}'.
                        format(activation_key)
                    )
                    return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(
                    {'detail': constants.ACTIVATION_KEY_NOT_EXPIRED}, status.HTTP_400_BAD_REQUEST
                )
        except UserenaSignup.DoesNotExist:
            return Response({'detail': constants.ACTIVATION_KEY_INVALID}, status.HTTP_400_BAD_REQUEST)


class ActivationResend(APIView):

    serializer_class = serializers.RequestEmailSerializer

    def post(self, request):

        try:

            serializer = self.serializer_class(data=request.DATA)

            if serializer.is_valid():

                try:
                    user = User.objects.get(email__iexact=serializer.validated_data['email'])

                except User.DoesNotExist:
                    raise AccountException(constants.EMAIL_UNKNOWN)

                if user.is_active:
                    raise AccountException(constants.USER_ACCOUNT_ALREADY_ACTIVATED)

                # handle deactivated account
                if user.profile.account_deactivated:
                    raise AccountException(constants.USER_ACCOUNT_DISABLED)

                new_activation_key = reissue_activation(user.userena_signup.activation_key)

                if new_activation_key:
                    send_activation_email(user, new_activation_key)
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    log_error('ERROR - activation key could not be generated for resend request for email {}'
                              .format(serializer.instance.email))
                    return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except AccountException as e:

            return Response({'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class Signin(APIView):

    serializer_class = serializers.AuthTokenSerializer

    def post(self, request):

        # block countries we are not licensed to operate in and tor clients
        if country_blocked(request) or is_tor_node(request):
            return Response(status=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        serializer = self.serializer_class(data=request.DATA)

        if serializer.is_valid():
            authenticated_user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=authenticated_user)
            return Response(
                {'token': token.key, 'id': authenticated_user.id})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signout(APIView):

    def post(self, request):

        if request.auth is not None:
            request.auth.delete()

        return Response()


@psa()
def auth_by_token(request, backend):

    user = request.backend.do_auth(
        access_token=request.DATA.get('access_token')
    )

    if user and user.is_active:
        return user
    else:
        return None


class SigninFacebook(APIView):

    def post(self, request, backend):

        auth_token = request.DATA.get('access_token', None)

        if auth_token and backend:

            try:
                user = auth_by_token(request, backend)

            except Exception, err:
                return Response({'detail': str(err)}, status=500)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'id': user.id})

            else:
                return Response({'detail': constants.SIGNIN_FACEBOOK_INVALID_TOKEN}, status=400)
        else:
            return Response({'detail': constants.INVALID_PARAMETERS}, status=400)

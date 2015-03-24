from django.conf import settings
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import User
from django.db import transaction as dbtransaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from userena.models import UserenaSignup
from userena.utils import generate_sha1, get_datetime_now

from account import serializers
from account import constants
from account.models import BeamProfile as Profile
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


class EmailChange(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        new_email = request.DATA.get('email', None)

        try:

            if not new_email:
                raise AccountException(constants.INVALID_PARAMETERS)
            if new_email.lower() == user.email:
                raise AccountException(constants.EMAIL_NOT_CHANGED)
            if User.objects.filter(email__iexact=new_email):
                raise AccountException(constants.EMAIL_IN_USE)

            # the following is a rewritten version of user.userena_signup.change_email(new_email)
            user.userena_signup.email_unconfirmed = new_email
            salt, hash = generate_sha1(user.username)
            user.userena_signup.email_confirmation_key = hash
            user.userena_signup.email_confirmation_key_created = get_datetime_now()
            user.userena_signup.save()

            # the purpose is rewriting the following part where the emails are sent out
            email_change_url = settings.USER_BASE_URL +\
                settings.MAIL_EMAIL_CHANGE_CONFIRM_URL.format(user.userena_signup.email_confirmation_key)

            context = {
                'user': user,
                'email_change_url': email_change_url
            }

            # mail to new email account
            mails.send_mail(
                subject_template_name=settings.MAIL_CHANGE_EMAIL_NEW_SUBJECT,
                email_template_name=settings.MAIL_CHANGE_EMAIL_NEW_TEXT,
                html_email_template_name=settings.MAIL_CHANGE_EMAIL_NEW_HTML,
                to_email=user.userena_signup.email_unconfirmed,
                from_email=settings.BEAM_MAIL_ADDRESS,
                context=context
            )

            context['support'] = settings.BEAM_SUPPORT_MAIL_ADDRESS
            context['new_email'] = user.userena_signup.email_unconfirmed

            # mail to old email account
            mails.send_mail(
                subject_template_name=settings.MAIL_CHANGE_EMAIL_OLD_SUBJECT,
                email_template_name=settings.MAIL_CHANGE_EMAIL_OLD_TEXT,
                html_email_template_name=settings.MAIL_CHANGE_EMAIL_OLD_HTML,
                to_email=user.email,
                from_email=settings.BEAM_MAIL_ADDRESS,
                context=context
            )
            return Response()

        except AccountException as e:
            return Response({'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirm(APIView):

    def get(self, request, *args, **kwargs):

        confirmation_key = kwargs['confirmation_key']

        user = UserenaSignup.objects.confirm_email(confirmation_key)
        if user:
            return Response()

        return Response({'detail': constants.INVALID_PARAMETERS}, status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    'DRF version of django.contrib.auth.views.password_reset'

    serializer_class = serializers.RequestEmailSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.DATA)

            if serializer.is_valid():

                try:
                    user = User.objects.get(email__iexact=serializer.validated_data['email'])

                except User.DoesNotExist:
                    raise AccountException(constants.EMAIL_UNKNOWN)

                if user.profile.account_deactivated:
                    raise AccountException(constants.USER_ACCOUNT_DISABLED)

                if not user.is_active:
                    raise AccountException(constants.USER_ACCOUNT_NOT_ACTIVATED_YET)

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                password_reset_url = settings.USER_BASE_URL +\
                    settings.MAIL_PASSWORD_RESET_URL.format(uid, token)

                context = {
                    'password_reset_url': password_reset_url,
                    'first_name': user.first_name,
                }

                mails.send_mail(
                    subject_template_name=settings.MAIL_PASSWORD_RESET_SUBJECT,
                    email_template_name=settings.MAIL_PASSWORD_RESET_TEXT,
                    html_email_template_name=settings.MAIL_PASSWORD_RESET_HTML,
                    context=context,
                    from_email=settings.BEAM_MAIL_ADDRESS,
                    to_email=user.email
                )

                return Response()

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except AccountException as e:
            return Response({'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(APIView):
    'DRF version of django.contrib.auth.views.password_reset_confirm'

    serializer_class = serializers.SetPasswordSerializer

    def _get_user(self, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            return user

        return None

    def get(self, request, *args, **kwargs):

        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        if self._get_user(uidb64, token):
            return Response()

        return Response({'detail': constants.INVALID_PARAMETERS}, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):

        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        user = self._get_user(uidb64, token)

        if not user:
            return Response({'detail': constants.INVALID_PARAMETERS})

        serializer = self.serializer_class(user=user, data=request.DATA)

        if serializer.is_valid():

            user.set_password(request.DATA['password1'])
            user.save()

            return Response()

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(APIView):

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        user = request.user
        serializer = self.serializer_class(user=user, data=request.DATA)

        if serializer.is_valid():

            user.set_password(request.DATA['password1'])
            user.save()

            # issue new token for user
            request.auth.delete()
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProfileView(RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self, queryset=None):
        user = self.request.user
        return User.objects.get(id=user.id)

    def update(self, request, *args, **kwargs):

        with dbtransaction.atomic():

            response = super(ProfileView, self).update(request, args, kwargs)

            if response.status_code == status.HTTP_200_OK:
                # clear response data
                response.data = {}

        return response

    def destroy(self, request, *args, **kwargs):
        '''
        customized to set active=false and delete
        token upon deletion of a user
        '''

        obj = self.get_object()

        # deactiveate users
        obj.is_active = False
        obj.save()

        # delete authentication token
        if request.auth is not None:
            request.auth.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

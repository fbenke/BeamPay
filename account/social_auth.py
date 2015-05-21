import requests

from django.conf import settings

from social.apps.django_app.utils import psa
from social.utils import parse_qs

from userena import settings as userena_settings
from userena.models import UserenaSignup

from account import constants
from account.models import BeamProfile as Profile
from account.utils import AccountException

from beam_value.utils.exceptions import APIException


@psa()
def auth_by_token(request, backend):

    key, secret = request.backend.get_key_and_secret()

    response = requests.get(request.backend.ACCESS_TOKEN_URL, params={
        'client_id': key,
        'redirect_uri': request.data.get('redirect_uri'),
        'client_secret': secret,
        'code': request.data.get('code')
    })

    try:
        response = response.json()
    except ValueError:
        response = parse_qs(response.text)

    try:
        access_token = response['access_token']
        return request.backend.do_auth(access_token)

    except KeyError:
        raise APIException(response['error']['message'])


def reject_no_email(backend, user, response, *args, **kwargs):

    if backend.name == settings.SOCIAL_AUTH_FACEBOOK:

        if not response.get('email'):
            raise AccountException(constants.SIGNIN_FACEBOOK_NO_EMAIL)


def reject_not_verified(backend, user, response, *args, **kwargs):

    if backend.name == settings.SOCIAL_AUTH_FACEBOOK:

        if not response.get('verified'):
            raise AccountException(constants.SIGNIN_FACEBOOK_NOT_VERIFIED)


def save_profile(backend, user, response, *args, **kwargs):

    # if necessary, create an empty profile
    try:
        new_profile = user.profile

    except Profile.DoesNotExist:
        new_profile = Profile(user=user)
        new_profile.save()

    # populate profile with Facebook data
    if backend.name == settings.SOCIAL_AUTH_FACEBOOK:
        new_profile.gender = response.get('gender')
        new_profile.facebook_link = response.get('link')
        new_profile.save()

    try:
        userena_signup = user.userena_signup

    except UserenaSignup.DoesNotExist:
        userena_signup = UserenaSignup(
            user=user,
            activation_key=userena_settings.USERENA_ACTIVATED
        )
        userena_signup.save()

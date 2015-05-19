import requests
from urlparse import parse_qs

from django.conf import settings

from social.apps.django_app.utils import psa

from userena import settings as userena_settings
from userena.models import UserenaSignup

from account.models import BeamProfile as Profile
from account.utils import AccountException

from beam_value.utils.exceptions import APIException


@psa()
def auth_by_token(request, backend):

    key, secret = request.backend.get_key_and_secret()
    r = requests.get(request.backend.ACCESS_TOKEN_URL, params={
        'client_id': key,
        'redirect_uri': request.DATA.get('redirect_uri'),
        'client_secret': secret,
        'code': request.DATA.get('code')
    })

    try:
        r = r.json()
    except ValueError:
        r = parse_qs(r.text)

    #
    # TODO: Falk, you might wanna log errors if access_token is not found in
    # `r`. Example, if there is something wrong with the FB app settings, you
    # may get an error as such:
    #
    # {
    #  "error":
    #   {
    #     "message":"Error validating verification code. Please make sure your
    #         redirect_uri is identical to the one you used in the OAuth dialog
    #         request",
    #     "type":"OAuthException",
    #     "code":100
    #  }
    # }
    #

    access_token = r['access_token']

    return request.backend.do_auth(access_token)


def reject_no_email(backend, user, response, *args, **kwargs):

    if backend.name == settings.SOCIAL_AUTH_FACEBOOK:

        if not response.get('email'):
            raise AccountException()


def reject_not_verified(backend, user, response, *args, **kwargs):

    if backend.name == settings.SOCIAL_AUTH_FACEBOOK:

        if not response.get('verified'):
            raise APIException()


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

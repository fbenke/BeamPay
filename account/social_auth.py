from django.conf import settings

from social.apps.django_app.utils import psa

from account.models import BeamProfile as Profile

from beam_value.utils.exceptions import APIException


@psa()
def auth_by_token(request, backend):

    return request.backend.do_auth(access_token=request.DATA.get('access_token'))


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

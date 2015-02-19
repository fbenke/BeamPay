from hashlib import sha1 as sha_constructor
import random
import re

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import fields
from rest_framework import serializers

from userena import settings as userena_settings
from userena.models import UserenaSignup

from account import constants


class PasswordSerializer(serializers.Serializer):

    password1 = fields.CharField(label='Password')
    password2 = fields.CharField(label='Repeat password')

    def validate_password1(self, value):
        if not re.match(settings.PASSWORD_REGEX, value):
            raise serializers.ValidationError(constants.PASSWORD_FORMAT)
        return value

    def validate(self, data):
        '''
        Validates that the values entered into the two password fields match.
        '''

        if 'password1' in data and 'password2' in data:
            if data['password1'] != data['password2']:
                raise serializers.ValidationError(constants.PASSWORD_MISMATCH)
        return data


class SignupSerializer(PasswordSerializer):
    '''
    Serializer for creating a new user account.
    Basically ports userena.forms.SignupForm to a
    Serializer to work with Django Rest Framework.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice.
    '''
    email = fields.EmailField(label='Email')
    accepted_privacy_policy = fields.BooleanField(label='Privacy Policy accepted')

    def validate_email(self, value):
        'Validate that the e-mail address is unique.'

        if User.objects.filter(email__iexact=value):
            if UserenaSignup.objects.filter(user__email__iexact=value)\
               .exclude(activation_key=userena_settings.USERENA_ACTIVATED):
                raise serializers.ValidationError(constants.EMAIL_IN_USE_UNCONFIRMED)
            raise serializers.ValidationError(constants.EMAIL_IN_USE)
        return value

    def validate_accepted_privacy_policy(self, value):
        if not value:
            raise serializers.ValidationError(constants.PRIVACY_POLICY_NOT_ACCEPTED)
        return value

    def create(self, validated_data):

        ''' Generate a random username before falling back to parent signup form '''
        while True:
            username = sha_constructor(str(random.random())).hexdigest()[:5]
            try:
                User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                break

        new_user = UserenaSignup.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password1'],
            active=False,
            # will be done manually in the next step to allow more flexibiliy
            send_email=False
        )

        return new_user

from hashlib import sha1 as sha_constructor
import random
import re

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import fields
from rest_framework import serializers

from userena import settings as userena_settings
from userena.models import UserenaSignup

from account import constants
from account import models

from django_countries.fields import Country


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


class RequestEmailSerializer(serializers.Serializer):

    email = fields.EmailField(label='Email')


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


class AuthTokenSerializer(serializers.Serializer):
    '''
    customized version of standard rest serializer working
    with email instead of username

    see: https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/serializers.py
    '''

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        user = authenticate(identification=email, password=password)

        if user:

            if user.is_staff:
                raise serializers.ValidationError(constants.ADMIN_ACCOUNT)

            if user.profile.account_deactivated:
                raise serializers.ValidationError(constants.USER_ACCOUNT_DISABLED)

            if not user.is_active:
                raise serializers.ValidationError(constants.USER_ACCOUNT_NOT_ACTIVATED_YET)

            data['user'] = user
            return data

        else:
            raise serializers.ValidationError(constants.SIGNIN_WRONG_CREDENTIALS)


class SetPasswordSerializer(PasswordSerializer):

    '''
    Serializer for resetting password without entering the old one.
    Basically ports django.contrib.auth.forms.SetPasswordForm to a
    Serializer to work with Django Rest Framework.
    '''

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordSerializer, self).__init__(*args, **kwargs)


class ChangePasswordSerializer(SetPasswordSerializer):
    '''
    Serializer for resetting password by entering the old one.
    Basically ports django.contrib.auth.forms.PasswordChangeForm to a
    Serializer to work with Django Rest Framework.
    '''

    old_password = serializers.CharField(label='Old password')

    def validate_old_password(self, value):

        if not self.user.check_password(value):
            raise serializers.ValidationError(constants.PASSWORD_OLD_INCORRECT)

        return value


class CountryField(serializers.Field):

    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        return Country(code=data)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BeamProfile
        read_only_fields = ('gender',)
        read_and_write_fields = (
            'date_of_birth', 'phone_number', 'street', 'city',
            'post_code', 'country'
        )

        fields = read_only_fields + read_and_write_fields


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        read_only_fields = ('email', )
        read_and_write_fields = ('first_name', 'last_name', 'profile')

        fields = read_only_fields + read_and_write_fields

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if validated_data.get('profile'):

            profile = validated_data.get('profile')

            instance.profile.date_of_birth = profile.get('date_of_birth', instance.profile.date_of_birth)
            instance.profile.phone_number = profile.get('phone_number', instance.profile.phone_number)
            instance.profile.country = profile.get('country', instance.profile.country)
            instance.profile.street = profile.get('street', instance.profile.street)
            instance.profile.city = profile.get('city', instance.profile.city)
            instance.profile.post_code = profile.get('post_code', instance.profile.post_code)

            instance.profile.save()

        instance.save()

        return instance

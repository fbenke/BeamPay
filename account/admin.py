from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings

from userena.admin import UserenaAdmin

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from account.models import BeamProfile as Profile


class BeamProfileAdmin(admin.ModelAdmin):

    def user_url(self, obj):
        path = settings.API_BASE_URL + 'admin/auth/user'
        return '<a href="{}/{}/">{}</a>'.format(path, obj.user.id, obj.user.id)
    user_url.allow_tags = True
    user_url.short_description = 'user'

    def user_email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.id

    def name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    readonly_fields = (
        'user_url', 'user_email', 'name', 'country', 'accepted_privacy_policy',
        'date_of_birth', 'phone_number'
    )

    fields = readonly_fields

    list_display = ('user_id', 'user_email', 'country')

    list_display_links = ('user_email', )

admin.site.register(Profile, BeamProfileAdmin)


class CustomUserenaAdmin(UserenaAdmin):

    list_display = ('id', 'email', 'is_staff', 'is_active', 'date_joined')
    list_display_links = ('id', 'email')

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserenaAdmin)


class CustomTokenAdmin(TokenAdmin):

    def user_email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.id

    list_display = ('user_email', 'key', 'created')

    readonly_fields = ('user_id', 'user_email', 'key')
    fields = readonly_fields

try:
    admin.site.unregister(Token)
except admin.sites.NotRegistered:
    pass
admin.site.register(Token, CustomTokenAdmin)

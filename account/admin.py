from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings

from userena.admin import UserenaAdmin

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from account.models import BeamProfile as Profile


# def beam_trust_status(user):
#     return user.profile.get_trust_status_display()


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
        'user_url', 'user_email', 'name', 'street', 'city', 'post_code',
        'country', 'accepted_privacy_policy', 'date_of_birth', 'phone_number',
        'preferred_contact_method', 'preferred_contact_details', 'gender',
        'facebook_link'
    )

    fieldsets = (
        ('User', {
            'fields': ('user_url', 'user_email', 'name', 'trust_status')
        }),
        ('Profile', {
            'fields': ('street', 'city', 'post_code', 'country',
                       'date_of_birth', 'phone_number', 'preferred_contact_method',
                       'preferred_contact_details')
        }),
        ('Misc', {
            'classes': ('collapse',),
            'fields': ('gender', 'facebook_link', 'accepted_privacy_policy')
        })


    )

    search_fields = ('user_id', 'user_email')

    list_display = ('user_id', 'user_email', 'country', 'trust_status')

    list_display_links = ('user_email', )

admin.site.register(Profile, BeamProfileAdmin)


class CustomUserenaAdmin(UserenaAdmin):

    def profile_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{}</a>'.format(path, obj.profile.id, obj.profile.id)
    profile_url.allow_tags = True
    profile_url.short_description = 'profile'

    list_display = ('id', 'email', 'profile_url', 'is_staff', 'is_active', 'date_joined')
    list_display_links = ('id', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__trust_status')
    ordering = ('-id',)

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

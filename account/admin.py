from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

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

    def referral_url(self, obj):
        path = settings.API_BASE_URL + 'admin/referral/referral'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.user.referral.id, obj.user.referral.id)
    referral_url.allow_tags = True
    referral_url.short_description = 'Referral Link'

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
        'facebook_link', 'referral_url'
    )

    fieldsets = (
        ('User', {
            'fields': ('user_url', 'user_email', 'name', 'trust_status')
        }),
        ('Profile', {
            'fields': ('street', 'city', 'post_code', 'country',
                       'date_of_birth', 'phone_number',
                       'preferred_contact_method',
                       'preferred_contact_details')
        }),
        ('Misc', {
            'classes': ('collapse',),
            'fields': (
                'gender', 'facebook_link',
                'accepted_privacy_policy', 'referral_url')
        })
    )

    search_fields = ('user__id', 'user__email')

    list_display = ('user_id', 'user_email', 'country', 'trust_status')
    list_per_page = 20

admin.site.register(Profile, BeamProfileAdmin)


class CustomUserenaAdmin(UserenaAdmin):

    def profile_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.profile.id, obj.profile.id)

    def referral_url(self, obj):
        path = settings.API_BASE_URL + 'admin/referral/referral'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.referral.id, obj.referral.id)
    referral_url.allow_tags = True
    referral_url.short_description = 'Referral Link'

    def beam_trust_status(self, obj):
        return obj.profile.get_trust_status_display()

    profile_url.allow_tags = True
    profile_url.short_description = 'profile'

    readonly_fields = ('referral_url',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'referral_url')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'id', 'email', 'profile_url', 'is_staff', 'is_active',
        'beam_trust_status', 'date_joined')
    list_display_links = ('id', 'email')
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'profile__trust_status')
    list_per_page = 20
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
    list_per_page = 20

    search_fields = ('user__email',)

    readonly_fields = ('user_id', 'user_email', 'key')
    fields = readonly_fields

try:
    admin.site.unregister(Token)
except admin.sites.NotRegistered:
    pass
admin.site.register(Token, CustomTokenAdmin)

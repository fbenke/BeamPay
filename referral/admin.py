from django.conf import settings
from django.contrib import admin

from models import Referral


class ReferralFeeAdmin(admin.ModelAdmin):

    def user_email(self, obj):
        return obj.user.email

    user_email.allow_tags = True
    user_email.short_description = 'user'

    def no_free_transcations(self, obj):
        return obj.no_free_transcations

    no_free_transcations.allow_tags = True
    no_free_transcations.short_description = 'no of free transcations'

    def user_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.user.profile.id, obj.user.email
        )

    user_url.allow_tags = True
    user_url.short_description = 'user'

    list_display = ('id', 'user_email', 'code',
                    'credits_gained', 'credits_redeemed')

    readonly_fields = ('id', 'user_url', 'no_free_transcations',
                       'referred_by', 'referred_to')

    fields = ('id', 'user_url', 'code', 'credits_gained',
              'credits_redeemed', 'referred_by', 'referred_to',
              'no_free_transcations')

admin.site.register(Referral, ReferralFeeAdmin)

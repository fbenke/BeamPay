from django.conf import settings
from django.contrib import admin

from models import Referral


class ReferralFeeAdmin(admin.ModelAdmin):

    def user_email(self, obj):
        try:
            return obj.user.email
        except AttributeError:
            return ''

    user_email.allow_tags = True
    user_email.short_description = 'user'

    def free_transaction_no(self, obj):
        return obj.free_transaction_no

    free_transaction_no.allow_tags = True
    free_transaction_no.short_description = 'no of free transcations'

    def user_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.user.profile.id, obj.user.email
        )

    user_url.allow_tags = True
    user_url.short_description = 'user'

    list_display = ('id', 'user_email', 'code',
                    'credits_gained', 'credits_redeemed')

    readonly_fields = ('id', 'user_url', 'free_transaction_no',
                       'referred_by', 'referred_to')

    fields = ('id', 'user_url', 'code', 'credits_gained',
              'credits_redeemed', 'referred_by', 'referred_to',
              'free_transaction_no')

admin.site.register(Referral, ReferralFeeAdmin)

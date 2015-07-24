from django.conf import settings
from django.contrib import admin

from recipient.models import Recipient


class RecipientAdmin(admin.ModelAdmin):

    def user_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{}</a>'.format(path, obj.user.profile.id, obj.user.id)

    user_url.allow_tags = True
    user_url.short_description = 'user'

    readonly_fields = (
        'user_url', 'id', 'first_name', 'last_name', 'phone_number',
        'email', 'date_of_birth', 'relation'
    )

    list_display = ('id', 'first_name', 'last_name', 'phone_number')
    search_fields = ('phone_number', 'first_name', 'last_name')

    fieldsets = (
        (None, {
            'fields': ('user_url', 'id', 'first_name', 'last_name',
                       'phone_number', 'email')
        }),
        ('Reserved for Later', {
            'classes': ('collapse', ),
            'fields': ('date_of_birth', 'relation')
        })
    )


admin.site.register(Recipient, RecipientAdmin)

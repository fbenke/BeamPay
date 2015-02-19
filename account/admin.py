from django.contrib import admin
from django.conf import settings

from account.models import BeamProfile as Profile


class BeamProfileAdmin(admin.ModelAdmin):

    def user_url(self, obj):
        path = settings.API_BASE_URL + '/admin/auth/user'
        return '<a href="{}/{}/">{}</a>'.format(path, obj.user.id, obj.user.id)
    user_url.allow_tags = True
    user_url.short_description = 'user'

    def user_email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.id

    def user_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    readonly_fields = ('country', )

    list_display = ('user_id', 'user_email', 'country')

    list_display_links = ('user_email', )

admin.site.register(Profile, BeamProfileAdmin)

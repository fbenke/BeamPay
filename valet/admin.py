from django.contrib import admin

from valet.models import WhatsappRequest


class WhatsappRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['wap_number']


admin.site.register(WhatsappRequest, WhatsappRequestAdmin)

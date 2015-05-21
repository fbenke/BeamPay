from django.contrib import admin

from recipient.models import Recipient


class RecipientAdmin(admin.ModelAdmin):

    readonly_fields = (
        'id', 'first_name', 'last_name', 'phone_number',
        'email', 'date_of_birth', 'relation'
    )
    read_and_write_fields = ()
    fields = readonly_fields + read_and_write_fields
    list_display = ('id', 'first_name', 'last_name', 'phone_number')

admin.site.register(Recipient, RecipientAdmin)

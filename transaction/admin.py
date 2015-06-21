from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from transaction.forms import CommentInlineFormset
from transaction.models import Comment, AirtimeTopup
from transaction import constants as c


class CommentInline(GenericTabularInline):

    model = Comment
    readonly_fields = ('author', 'timestamp')
    extra = 1
    max_num = 10
    can_delete = True
    formset = CommentInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class GenericTransactionAdmin(admin.ModelAdmin):

    class Meta:
        abstract = True

    def sender_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{} {}</a>'.format(
            path, obj.sender.profile.id, obj.sender.first_name, obj.sender.last_name)

    sender_url.allow_tags = True
    sender_url.short_description = 'sender'

    def sender_email(self, obj):
        return obj.sender.email

    sender_email.allow_tags = True
    sender_email.short_description = 'sender'

    def recipient_name(self, obj):
        return '{} {}'.format(obj.recipient.first_name, obj.recipient.last_name)

    recipient_name.allow_tags = True
    recipient_name.short_description = 'recipient'

    def recipient_url(self, obj):
        path = settings.API_BASE_URL + 'admin/recipient/recipient'
        return '<a href="{}/{}/">{} {} ({})</a>'.format(
            path, obj.recipient.id, obj.recipient.first_name,
            obj.recipient.last_name, obj.recipient.id
        )

    recipient_url.allow_tags = True
    recipient_url.short_description = 'recipient'

    def exchange_rate_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/exchangerate'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.exchange_rate.id, obj.exchange_rate.usd_ghs)

    exchange_rate_url.allow_tags = True
    exchange_rate_url.short_description = 'exchange rate'

    def charge_usd(self, obj):
        return obj.charge_usd

    charge_usd.allow_tags = True
    charge_usd.short_description = 'charge in usd'

    #  default settings
    list_display = (
        'id', 'sender_email', 'recipient_name', 'reference_number', 'state'
    )

    list_filter = ('state',)

    search_fields = ('id', 'reference_number')

    list_per_page = 15

    inlines = (CommentInline, )

    readonly_fields = (
        'id', 'sender_url', 'recipient_url', 'exchange_rate_url',
        'total_charge_usd', 'reference_number', 'last_changed',
        'service_charge', 'payment_processor', 'payment_reference'
    )

    fieldsets = (
        (None, {
            'fields': ('id', 'sender_url', 'recipient_url',
                       'reference_number', 'state', 'last_changed')
        }),
        ('Pricing', {
            'fields': ('exchange_rate_url', 'amount_usd',
                       'amount_ghs', 'service_charge',
                       'total_charge_usd')
        }),
        ('Payments', {
            'fields': ('payment_processor', 'payment_reference')
        })
    )

    def save_model(self, request, obj, form, change):
        if 'state' in form.changed_data:
            obj.add_status_change(
                author=request.user,
                comment=getattr(obj, 'state')
            )

        # TODO: check
        if 'amount_ghs' in form.changed_data and getattr(obj, 'amount_ghs'):
            obj.amount_usd = getattr(obj, 'amount_ghs') / obj.exchange_rate.usd_ghs

        elif 'amount_usd' in form.changed_data and getattr(obj, 'amount_usd'):
            obj.amount_ghs = getattr(obj, 'amount_usd') * obj.exchange_rate.usd_ghs

        obj.save()


class AirtimeTopupAdmin(GenericTransactionAdmin):

    def __init__(self, model, admin_site):
        super(AirtimeTopupAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ('network', 'service_fee_url',
                                 'amount_usd', 'amount_ghs')
        addtl_fieldset = ('network', 'service_fee_url')
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('Airtime', {'fields': addtl_fieldset})
        self.fieldsets = (self.fieldsets[0], self.fieldsets[1],
                          addtl_fieldset, self.fieldsets[2])

    def service_fee_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/airtimeservicefee'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.airtime_service_fee.id, obj.airtime_service_fee.id)

    service_fee_url.allow_tags = True
    service_fee_url.short_description = 'service fee'

    def save_model(self, request, obj, form, change):
        super(AirtimeTopupAdmin, self).save_model(request, obj, form, change)

        if 'state' in form.changed_data and obj.state == c.PROCESSED:
            obj.post_processed()


admin.site.register(AirtimeTopup, AirtimeTopupAdmin)

from django.conf import settings
from django.contrib import admin
from django.utils import timezone

from transaction.forms import CommentInlineFormset, TransactionModelForm
from transaction.models import Transaction, Comment, AirtimeTopup


class CommentInline(admin.TabularInline):

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


class TransactionAdmin(admin.ModelAdmin):

    form = TransactionModelForm

    def sender_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{} {}</a>'.format(
            path, obj.sender.profile.id, obj.sender.first_name, obj.sender.last_name)

    sender_url.allow_tags = True
    sender_url.short_description = 'sender'

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

    def sender_email(self, obj):
        return obj.sender.email

    sender_email.allow_tags = True
    sender_email.short_description = 'sender email'

    def recipient_name(self, obj):
        return '{} {}'.format(obj.recipient.first_name, obj.recipient.last_name)

    recipient_name.allow_tags = True
    recipient_name.short_description = 'recipient name'

    readonly_fields = (
        'id', 'sender_url', 'recipient_url', 'exchange_rate_url', 'transaction_type',
        'reference_number', 'last_changed', 'additional_info', 'charge_usd'
    )

    fieldsets = (
        (None, {
            'fields': ('id', 'sender_url', 'recipient_url', 'transaction_type',
                       'reference_number', 'state', 'additional_info', 'last_changed')
        }),
        ('Pricing', {
            'fields': ('exchange_rate_url', 'cost_of_delivery_usd',
                       'cost_of_delivery_ghs', 'service_charge', 'charge_usd')
        }),
        ('Payments', {
            'fields': ('payment_processor', 'payment_reference')
        })
    )

    list_display = (
        'id', 'sender_email', 'recipient_name', 'transaction_type', 'reference_number', 'state'
    )

    list_filter = ('state',)

    search_fields = ('id', 'reference_number')

    list_per_page = 15

    inlines = (CommentInline, )

    def save_model(self, request, obj, form, change):

        if 'state' in form.changed_data:
            obj.add_status_change(
                author=request.user,
                comment=getattr(obj, 'state')
            )

        if 'cost_of_delivery_ghs' in form.changed_data and getattr(obj, 'cost_of_delivery_ghs'):
            obj.cost_of_delivery_usd = getattr(obj, 'cost_of_delivery_ghs') / obj.exchange_rate.usd_ghs

        elif 'cost_of_delivery_usd' in form.changed_data and getattr(obj, 'cost_of_delivery_usd'):
            obj.cost_of_delivery_ghs = getattr(obj, 'cost_of_delivery_usd') * obj.exchange_rate.usd_ghs

        obj.save()

admin.site.register(Transaction, TransactionAdmin)


class AirtimeTopupAdmin(admin.ModelAdmin):

    STATE_CHANGE_TIMESTAMP_FIELD = {
        Transaction.PROCESSED: 'processed_at',
        Transaction.PAID: 'paid_at',
        Transaction.CANCELLED: 'cancelled_at',
        Transaction.INVALID: 'invalidated_at'
    }

    def sender_email(self, obj):
        return obj.sender.email

    def sender_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{} {}</a>'.format(
            path, obj.sender.profile.id, obj.sender.first_name, obj.sender.last_name)

    sender_url.allow_tags = True
    sender_url.short_description = 'sender'

    def exchange_rate_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/exchangerate'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.exchange_rate.id, obj.exchange_rate.usd_ghs)

    exchange_rate_url.allow_tags = True
    exchange_rate_url.short_description = 'exchange rate'

    def service_fee_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/airtimeservicefee'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.service_fee.id, obj.service_fee.fee)

    service_fee_url.allow_tags = True
    service_fee_url.short_description = 'service fee'

    def charge_usd(self, obj):
        return obj.charge_usd

    charge_usd.allow_tags = True
    charge_usd.short_description = 'charge in usd'

    readonly_fields = (
        'id', 'sender_url', 'exchange_rate_url', 'service_fee_url',
        'phone_number', 'network', 'amount_ghs', 'reference_number',
        'initialized_at', 'paid_at', 'processed_at', 'cancelled_at',
        'invalidated_at', 'charge_usd', 'payment_processor', 'payment_reference'
    )

    fieldsets = (
        (None, {
            'fields': ('sender_url', 'phone_number', 'network', 'reference_number')
        }),
        ('Pricing', {
            'fields': ('exchange_rate_url', 'service_fee_url', 'amount_ghs', 'charge_usd')
        }),
        ('Payments', {
            'fields': ('payment_processor', 'payment_reference')
        }),
        ('State', {
            'fields': ('state', 'initialized_at', 'paid_at', 'processed_at',
                       'cancelled_at', 'invalidated_at', 'comments')
        })
    )

    list_display = ('id', 'sender_email', 'reference_number', 'state')

    list_filter = ('state',)

    search_fields = ('id', 'reference_number')

    list_per_page = 15

    def save_model(self, request, obj, form, change):

        if 'state' in form.changed_data:

            timestamp_field = self.STATE_CHANGE_TIMESTAMP_FIELD[getattr(obj, 'state')]
            setattr(obj, timestamp_field, timezone.now())

            if obj.state == Transaction.PROCESSED:
                obj.post_processed()

        obj.save()

admin.site.register(AirtimeTopup, AirtimeTopupAdmin)

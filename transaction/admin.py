from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from transaction.forms import CommentInlineFormset
from transaction import models

from pricing.models import get_current_exchange_rate


class CommentInline(GenericTabularInline):

    model = models.Comment
    readonly_fields = ('author', 'timestamp')
    extra = 1
    max_num = 10
    can_delete = True
    formset = CommentInlineFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(
            request, obj, **kwargs)
        formset.request = request
        return formset


class GenericTransactionAdmin(admin.ModelAdmin):

    class Meta:
        abstract = True

    def sender_url(self, obj):
        path = settings.API_BASE_URL + 'admin/account/beamprofile'
        return '<a href="{}/{}/">{} {}</a>'.format(
            path, obj.sender.profile.id, obj.sender.first_name,
            obj.sender.last_name)

    sender_url.allow_tags = True
    sender_url.short_description = 'sender'

    def contact_method(self, obj):

        return '{}: {}'.format(
            obj.sender.profile.preferred_contact_method,
            obj.sender.profile.preferred_contact_details)

    contact_method.allow_tags = True
    contact_method.short_description = 'contact via'

    def sender_email(self, obj):
        return obj.sender.email

    sender_email.allow_tags = True
    sender_email.short_description = 'sender'

    def recipient_name(self, obj):
        return '{} {}'.format(
            obj.recipient.first_name, obj.recipient.last_name)

    recipient_name.allow_tags = True
    recipient_name.short_description = 'recipient'

    def recipient_url(self, obj):
        path = settings.API_BASE_URL + 'admin/recipient/recipient'
        return '<a href="{}/{}/">{} {} (id:{})</a>'.format(
            path, obj.recipient.id, obj.recipient.first_name,
            obj.recipient.last_name, obj.recipient.id
        )

    recipient_url.allow_tags = True
    recipient_url.short_description = 'recipient'

    def exchange_rate_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/exchangerate'
        return '<a href="{}/{}/">{} (id:{})</a>'.format(
            path, obj.exchange_rate.id, obj.exchange_rate.usd_ghs,
            obj.exchange_rate.id)

    exchange_rate_url.allow_tags = True
    exchange_rate_url.short_description = 'exchange rate'

    def referral_url(self, obj):
        path = settings.API_BASE_URL + 'admin/referral/referral'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.sender.referral.id,
            obj.sender.referral.no_free_transcations)

    referral_url.allow_tags = True
    referral_url.short_description = 'free transactions'

    def charge_usd(self, obj):
        return obj.charge_usd

    charge_usd.allow_tags = True
    charge_usd.short_description = 'charge in usd'

    #  default settings
    list_display = (
        'id', 'sender_email', 'recipient_name', 'reference_number', 'state'
    )

    list_filter = ('state', 'free_from_referral')

    search_fields = ('id', 'reference_number')

    list_per_page = 15

    inlines = (CommentInline, )

    readonly_fields = (
        'id', 'sender_url', 'recipient_url', 'exchange_rate_url',
        'total_charge_usd', 'reference_number', 'last_changed',
        'contact_method', 'referral_url'
    )

    fieldsets = (
        (None, {
            'fields': ('id', 'sender_url', 'contact_method', 'recipient_url',
                       'reference_number', 'state', 'last_changed')
        }),
        ('Pricing', {
            'fields': ('exchange_rate_url', 'amount_ghs',
                       'amount_usd', 'service_charge',
                       'total_charge_usd', 'referral_url')
        }),
        ('Payments', {
            'fields': ('payment_processor', 'payment_reference')
        }),
        ('Operations', {
            'fields': ('remarks', )
        })
    )

    def save_model(self, request, obj, form, change):

        if 'state' in form.changed_data:
            obj.add_status_change(
                author=request.user,
                comment=getattr(obj, 'state')
            )

        if 'amount_ghs' in form.changed_data and getattr(obj, 'amount_ghs'):
            obj.exchange_rate = get_current_exchange_rate()
            obj.amount_usd = getattr(obj, 'amount_ghs') / obj.exchange_rate.usd_ghs

        elif 'amount_usd' in form.changed_data and getattr(obj, 'amount_usd'):
            obj.exchange_rate = get_current_exchange_rate()
            obj.amount_ghs = getattr(obj, 'amount_usd') * obj.exchange_rate.usd_ghs

        obj.save()


class InstantPaymentAdmin(GenericTransactionAdmin):

    def __init__(self, model, admin_site):
        super(InstantPaymentAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ('service_fee_url', 'service_charge',
                                 'amount_usd', 'amount_ghs',
                                 'payment_processor', 'payment_reference',
                                 'free_from_referral')
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields

        pricing_fieldset = ('Pricing', {
            'fields': ('free_from_referral', 'exchange_rate_url',
                       'service_fee_url', 'amount_ghs', 'amount_usd',
                       'service_charge', 'total_charge_usd')
        })

        self.fieldsets = (self.fieldsets[0], pricing_fieldset,
                          self.fieldsets[2], self.fieldsets[3])

    def service_fee_url(self, obj):
        path = settings.API_BASE_URL + 'admin/pricing/servicefee'
        return '<a href="{}/{}/">{}</a>'.format(
            path, obj.service_fee.id, obj.service_fee.id)

    service_fee_url.allow_tags = True
    service_fee_url.short_description = 'service fee'


class AirtimeTopupAdmin(InstantPaymentAdmin):

    def __init__(self, model, admin_site):
        super(AirtimeTopupAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ('network', 'phone_number')
        addtl_fieldset = ('phone_number', 'network')
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('Airtime', {'fields': addtl_fieldset})
        self.fieldsets = (self.fieldsets[0], addtl_fieldset,
                          self.fieldsets[1], self.fieldsets[2],
                          self.fieldsets[3])


class BillPaymentAdmin(InstantPaymentAdmin):

    def __init__(self, model, admin_site):
        super(BillPaymentAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ('bill_type', )
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('bill_type', 'account_number', 'reference')
        addtl_fieldset = ('Bill', {'fields': addtl_fieldset})
        self.fieldsets = (self.fieldsets[0], addtl_fieldset,
                          self.fieldsets[1], self.fieldsets[2],
                          self.fieldsets[3])


class ValetAdmin(GenericTransactionAdmin):

    def __init__(self, model, admin_site):
        super(ValetAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ('description', )
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('description', )
        addtl_fieldset = ('Valet', {'fields': addtl_fieldset})
        pricing_fieldset = (
            'Pricing', {
                'fields': (
                    'free_from_referral', 'exchange_rate_url', 'amount_ghs',
                    'amount_usd', 'service_charge', 'total_charge_usd',
                    'referral_url')
            }
        )
        self.fieldsets = (self.fieldsets[0], addtl_fieldset,
                          pricing_fieldset, self.fieldsets[2],
                          self.fieldsets[3])


class SchoolFeeAdmin(GenericTransactionAdmin):

    def __init__(self, model, admin_site):
        super(SchoolFeeAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ()
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('ward_name', 'school', 'additional_info')
        addtl_fieldset = ('School Fees', {'fields': addtl_fieldset})
        pricing_fieldset = (
            'Pricing', {
                'fields': (
                    'free_from_referral', 'exchange_rate_url', 'amount_ghs',
                    'amount_usd', 'service_charge', 'total_charge_usd',
                    'referral_url')
            }
        )
        self.fieldsets = (self.fieldsets[0], addtl_fieldset,
                          pricing_fieldset, self.fieldsets[2],
                          self.fieldsets[3])


class GiftAdmin(GenericTransactionAdmin):

    def __init__(self, model, admin_site):
        super(GiftAdmin, self).__init__(model, admin_site)
        addtl_readonly_fields = ()
        self.readonly_fields = self.readonly_fields + addtl_readonly_fields
        addtl_fieldset = ('gift_type', 'delivery_address',
                          'delivery_time', 'additional_info')
        addtl_fieldset = ('Gift', {'fields': addtl_fieldset})
        pricing_fieldset = (
            'Pricing', {
                'fields': (
                    'free_from_referral', 'exchange_rate_url', 'amount_ghs',
                    'amount_usd', 'service_charge', 'total_charge_usd',
                    'referral_url')
            }
        )
        self.fieldsets = (self.fieldsets[0], addtl_fieldset,
                          pricing_fieldset, self.fieldsets[2],
                          self.fieldsets[3])

admin.site.register(models.AirtimeTopup, AirtimeTopupAdmin)
admin.site.register(models.ValetTransaction, ValetAdmin)
admin.site.register(models.SchoolFeePayment, SchoolFeeAdmin)
admin.site.register(models.BillPayment, BillPaymentAdmin)
admin.site.register(models.Gift, GiftAdmin)

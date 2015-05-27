from django.contrib import admin

from pricing.models import ExchangeRate, AirtimeServiceFee, end_previous_object


class DoNotDeleteModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(DoNotDeleteModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class ExchangeRateAdmin(DoNotDeleteModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('id', 'start', 'end', 'usd_ghs')
        else:
            return ('id', 'start', 'end')

    list_display = ('id', 'start', 'end', 'usd_ghs')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            end_previous_object(ExchangeRate)
            obj.save()

admin.site.register(ExchangeRate, ExchangeRateAdmin)


class AirtimeServiceFeeAdmin(DoNotDeleteModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('id', 'start', 'end', 'fee')
        else:
            return ('id', 'start', 'end')

    list_display = ('id', 'start', 'end', 'fee')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            end_previous_object(AirtimeServiceFee)
            obj.save()

admin.site.register(AirtimeServiceFee, AirtimeServiceFeeAdmin)

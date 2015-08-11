from django.contrib import admin

from pricing.models import ExchangeRate, ServiceFee, end_previous_object


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


class ServiceFeeAdmin(DoNotDeleteModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('id', 'start', 'end', 'fixed_fee', 'percentual_fee')
        else:
            return ('id', 'start', 'end')

    list_display = (
        'id', 'service', 'start', 'end', 'fixed_fee', 'percentual_fee')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            end_previous_object(ServiceFee, obj)
            obj.save()

admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(ServiceFee, ServiceFeeAdmin)

from django.conf.urls import patterns, url
from payment import views

urlpatterns = patterns(
    '',
    # url(
    #     r'^stripe/charge_txn/$',
    #     views.StripeChargeTransaction.as_view(),
    #     name='stripe_charge_txn'
    # ),
    url(
        r'^stripe/charge_airtime/$',
        views.StripeChargeAirtime.as_view(),
        name='stripe_charge_airtime'
    ),
)

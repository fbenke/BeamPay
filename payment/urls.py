from django.conf.urls import patterns, url
from payment import views

urlpatterns = patterns(
    '',
    url(
        r'^stripe/$',
        views.StripeCharge.as_view(),
        name='stripe'
    ),
)

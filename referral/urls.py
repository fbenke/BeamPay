from django.conf.urls import patterns, url
from django.contrib import admin

from referral import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.ViewReferral.as_view(),
        name='get'
    ),
    url(
        r'^add/$',
        views.AddReferral.as_view(),
        name='add'
    ),
    url(
        r'^status/$',
        views.ReferralStatus.as_view(),
        name='status'
    )
)

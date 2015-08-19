from django.conf.urls import patterns, url
from django.contrib import admin

from transaction import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^add/airtime/$',
        views.CreateAirtimeTopup.as_view(),
        name='add_airtime'
    ),
    url(
        r'^add/bill/$',
        views.CreateBillPayment.as_view(),
        name='add_bill'
    ),
    url(
        r'^add/gift/$',
        views.CreateGiftOrder.as_view(),
        name='add_gift'
    ),
    url(
        r'^add/school/$',
        views.CreateSchoolFeePayment.as_view(),
        name='add_school_fee'
    ),
    url(
        r'^add/valet/$',
        views.CreateValetTransaction.as_view(),
        name='add_valet'
    ),
    url(
        r'^setup/$',
        views.InstaPaySetupView.as_view(),
        name='setup'
    ),
    url(
        r'^$',
        views.ViewTransactions.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        views.GetTransaction.as_view(),
        name='get'
    )
)

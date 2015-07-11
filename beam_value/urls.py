from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from beam_value import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='home'
    ),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots'
    ),
    url(
        r'^humans\.txt$',
        TemplateView.as_view(template_name='humans.txt', content_type='text/plain'),
        name='humans'
    ),
    url(
        r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.png')
    ),
    url(
        r'^share_mail/$',
        views.ShareViaEmailView.as_view(),
        name='share_via_email'
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^api/v1/account/',
        include('account.urls', namespace='account')
    ),
    url(
        r'^api/v1/pricing/',
        include('pricing.urls', namespace='pricing')
    ),
    url(
        r'^api/v1/payment/',
        include('payment.urls', namespace='payment')
    ),
    url(
        r'^api/v1/transaction/',
        include('transaction.urls', namespace='transaction')
    ),
    url(
        r'^api/v1/recipient/',
        include('recipient.urls', namespace='recipient')
    ),
    url(
        r'^api/v1/referral/',
        include('referral.urls', namespace='referral')
    )
)

handler404 = 'beam.views.page_not_found'
handler500 = 'beam.views.custom_error'
handler403 = 'beam.views.permission_denied'
handler400 = 'beam.views.bad_request'

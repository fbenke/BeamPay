from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from account import views

urlpatterns = patterns(
    '',
    url(
        r'^signup/$',
        views.Signup.as_view(),
        name='signup'
    ),
    url(
        r'^activate/retry/(?P<activation_key>\w+)/$',
        views.ActivationRetry.as_view(),
        name='activate_retry'
    ),
    url(
        r'^activate/resend/$',
        views.ActivationResend.as_view(),
        name='activate_resend'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        views.Activation.as_view(),
        name='activate'
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns)

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
)

urlpatterns = format_suffix_patterns(urlpatterns)

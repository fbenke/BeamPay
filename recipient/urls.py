from django.conf.urls import patterns, url
from django.contrib import admin

from recipient import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.ViewRecipients.as_view(),
        name='list'
    )
)

from django.conf.urls import patterns, url
from django.contrib import admin

from valet import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^add/number/$',
        views.add_whatsapp_number,
        name='add_number'
    )
)

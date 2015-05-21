from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from beam_value.utils.log import log_error


def get_current_object(cls):
    try:
        return cls.objects.get(end__isnull=True)
    except ObjectDoesNotExist:
        log_error('ERROR {} - No pricing object found.'.format(cls))
        raise ObjectDoesNotExist


def end_previous_object(cls):
    try:
        previous_object = cls.objects.get(end__isnull=True)
        previous_object.end = timezone.now()
        previous_object.save()
    except ObjectDoesNotExist:
        if cls.objects.all().exists():
            log_error('ERROR {} - Failed to end previous pricing.'.format(cls))
            raise ObjectDoesNotExist


class ExchangeRate(models.Model):

    start = models.DateTimeField(
        'Start Time',
        auto_now_add=True,
        help_text='Time at which exchange rate came into effect.'
    )

    end = models.DateTimeField(
        'End Time',
        blank=True,
        null=True,
        help_text='Time at which exchange rate came ended. If null, it represents the current exchange rate.' +
                  'Only one row in this table can have a null value for this column.'
    )

    usd_ghs = models.FloatField(
        'USD to GHS Exchange Rate',
        help_text='Exchange Rate from USD to GHS without markup'
    )

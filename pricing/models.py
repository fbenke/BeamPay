from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from beam_value.utils.log import log_error


def get_current_object(cls):
    try:
        return cls.objects.get(end__isnull=True)

    except ObjectDoesNotExist:
        msg = 'ERROR {} - No pricing object found.'.format(cls)
        log_error(msg)
        raise ObjectDoesNotExist(msg)


def end_previous_object(cls):
    try:
        previous_object = cls.objects.get(end__isnull=True)
        previous_object.end = timezone.now()
        previous_object.save()
    except ObjectDoesNotExist:
        if cls.objects.all().exists():
            msg = 'ERROR {} - Failed to end previous pricing.'.format(cls)
            log_error(msg)
            raise ObjectDoesNotExist(msg)


def get_current_exchange_rate():
    return get_current_object(ExchangeRate)


def get_current_airtime_fee():
    return get_current_object(AirtimeServiceFee)


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
        help_text='Time at which exchange rate came ended.'
    )

    usd_ghs = models.FloatField(
        'USD to GHS Exchange Rate',
        help_text='Exchange Rate from USD to GHS without markup'
    )


class AirtimeServiceFee(models.Model):

    start = models.DateTimeField(
        'Start Time',
        auto_now_add=True,
        help_text='Time at which pricing structure came into effect'
    )

    end = models.DateTimeField(
        'End Time',
        blank=True,
        null=True,
        help_text='Time at which pricing ended.'
    )

    fee = models.FloatField(
        'Service Fee in USD',
        help_text='Service fee charged for the airtime topup.'
    )

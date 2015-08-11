from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from beam_value.utils.log import log_error
from pricing.exceptions import ObjectsDoNotExist
from pricing import constants as c


def get_current_object(cls):
    try:
        return cls.objects.get(end__isnull=True)

    except ObjectDoesNotExist:
        msg = 'ERROR {} - No pricing object found.'.format(cls)
        log_error(msg)
        raise ObjectDoesNotExist(msg)


def get_current_objects(cls):
    objs = cls.objects.filter(end__isnull=True)

    if len(objs) < 2:
        print objs
        msg = 'ERROR {} - No pricing object found.'.format(cls)
        log_error(msg)
        raise ObjectsDoNotExist(msg)

    return objs


def end_previous_object(cls, obj):
    try:
        previous_object = cls.objects.get(
            end__isnull=True, service=obj.service)
        previous_object.end = timezone.now()
        previous_object.save()
    except ObjectDoesNotExist:
        if cls.objects.filter(service=obj.service).exists():
            msg = 'ERROR {} - Failed to end previous pricing.'.format(cls)
            log_error(msg)
            raise ObjectDoesNotExist(msg)
        pass


def get_current_exchange_rate():
    return get_current_object(ExchangeRate)


def get_current_service_fees():
    return get_current_objects(ServiceFee)


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


class ServiceFee(models.Model):

    start = models.DateTimeField(
        'Start Time',
        auto_now_add=True,
        help_text='Time at which pricing structure came into effect'
    )

    service = models.CharField(
        'Service',
        max_length=10,
        choices=c.PRICING_TYPE,
        default=c.AIRTIME,
        help_text='The service which the fee is for.'
    )

    end = models.DateTimeField(
        'End Time',
        blank=True,
        null=True,
        help_text='Time at which pricing ended.'
    )

    fixed_fee = models.FloatField(
        'Service fee in USD',
        help_text='Service fee charged for the airtime topup.'
    )

    percentual_fee = models.FloatField(
        'Percentual fee',
        help_text='Percentual amount to be added as charge.\
        Value between 0 and 1.'
    )

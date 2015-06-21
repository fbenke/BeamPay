from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from beam_value.utils import mails

from pricing.models import ExchangeRate, AirtimeServiceFee

from recipient.models import Recipient

from transaction import constants as c


class AbstractTransaction(models.Model):

    class Meta:
        ordering = ['-last_changed']
        abstract = True

    PAYMENT_PROCESSOR_CHOICES = (
        (c.PAYPAL, 'paypal'),
        (c.STRIPE, 'stripe'),
        (c.WEPAY, 'wepay')
    )

    TRANSACTION_STATES = (
        (c.INIT, 'initialized'),
        (c.GATHERING_INFO, 'gatering information'),
        (c.READY_FOR_PAYMENT, 'ready for payment'),
        (c.PAID, 'paid'),
        (c.PROCESSED, 'processed'),
        (c.CANCELLED, 'cancelled'),
        (c.INVALID, 'invalid')
    )

    sender = models.ForeignKey(
        User,
        related_name='%(app_label)s_%(class)s',
        help_text='Sender associated with that transaction'
    )

    recipient = models.ForeignKey(
        Recipient,
        related_name='%(app_label)s_%(class)s',
        help_text='Recipient associated with that transaction'
    )

    state = models.CharField(
        'State',
        max_length=4,
        choices=TRANSACTION_STATES,
        default=c.INIT,
        help_text='State of the transaction.'
    )

    reference_number = models.CharField(
        'Reference Number',
        max_length=6,
        help_text='6-digit reference number given to the customer to refer ' +
                  'to transaction in case of problems'
    )

    exchange_rate = models.ForeignKey(
        ExchangeRate,
        related_name='%(app_label)s_%(class)s',
        help_text='Exchange rate applied to this transaction',
        null=True
    )

    service_charge = models.FloatField(
        'Service charge in USD',
        blank=True,
        null=True,
        help_text='Service charge of the transaction in USD'
    )

    amount_usd = models.FloatField(
        'Cost of transaction in USD',
        blank=True,
        null=True,
        help_text='Cost of the transaction in USD.\
        This could be the cost of the service or product we pay for\
        on behalf of the sender.'
    )

    amount_ghs = models.FloatField(
        'Cost of transaction in GHS',
        blank=True,
        null=True,
        help_text='Cost of the transaction in GHS.'
    )

    payment_processor = models.CharField(
        'Payment Processor',
        max_length=4,
        blank=True,
        choices=PAYMENT_PROCESSOR_CHOICES,
        help_text='Payment Processor used'
    )

    payment_reference = models.CharField(
        'Payment Reference',
        max_length=50,
        blank=True,
        help_text='Reference generated by payment processor'
    )

    last_changed = models.DateTimeField(
        'Last changed',
        auto_now_add=True,
        help_text='Last changed'
    )

    def save(self, *args, **kwargs):
        self.last_changed = timezone.now()
        super(AbstractTransaction, self).save(*args, **kwargs)

    def add_status_change(self, comment, author='user'):
        ctype = ContentType.objects.get_for_model(self)

        comment = Comment(
            content_type=ctype,
            object_id=self.id,
            author=author,
            comment=comment
        )

        comment.save()

    @property
    def total_charge_usd(self):
        try:
            return self.amount_usd + self.service_charge
        except TypeError:
            return None


class AirtimeTopup(AbstractTransaction):

    NETWORK_CHOICES = (
        (c.VODAFONE, 'Vodafone'),
        (c.AIRTEL, 'Airtel'),
        (c.MTN, 'MTN'),
        (c.TIGO, 'Tigo')
    )

    network = models.CharField(
        'Network',
        max_length=4,
        choices=NETWORK_CHOICES,
        help_text='Phone Network'
    )

    airtime_service_fee = models.ForeignKey(
        AirtimeServiceFee,
        related_name='airtime_topup',
        help_text='Service fee applied to this topup'
    )

    # TODO: revisit
    def post_paid(self):

        mails.send_mail(
            subject_template_name=settings.MAIL_NOTIFY_ADMIN_PAID_SUBJECT,
            email_template_name=settings.MAIL_NOTIFY_ADMIN_PAID_TEXT,
            context={
                'domain': settings.ENV_SITE_MAPPING[settings.ENV][settings.SITE_API],
                'protocol': settings.PROTOCOL,
                'id': self.id
            },
            to_email=mails.get_admin_mail_addresses()
        )

    def post_processed(self):

        context = {
            'first_name': self.sender.first_name,
            'amount_ghs': self.amount_ghs,
            'phone_number': self.recipient.phone_number,
        }

        mails.send_mail(
            subject_template_name=settings.MAIL_AITRIME_TOPUP_COMPLETE_SUBJECT,
            email_template_name=settings.MAIL_AITRIME_TOPUP_COMPLETE_TEXT,
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=self.sender.email,
            html_email_template_name=settings.MAIL_AITRIME_TOPUP_COMPLETE_HTML
        )


class ValetTransaction(AbstractTransaction):

    description = models.CharField(
        'Description',
        max_length=500,
        blank=True,
        help_text='Description of the valet request'
    )


class Comment(models.Model):

    class Meta:
        ordering = ['-timestamp']

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    author = models.CharField(
        'Author',
        max_length=50,
        help_text='Author of comment'
    )

    timestamp = models.DateTimeField(
        'Timestamp',
        auto_now_add=True,
        help_text='Timestamp of comment'
    )

    comment = models.CharField(
        'Comment',
        max_length=300,
        help_text='The comment itself'
    )

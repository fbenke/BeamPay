from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from pricing.models import ExchangeRate, AirtimeServiceFee

from recipient.models import Recipient


class AirtimeTopup(models.Model):

    class Meta:
        ordering = ['-initialized_at']

    # Constants
    VODAFONE = 'VOD'
    AIRTEL = 'AIR'
    MTN = 'MTN'

    NETWORK_CHOICES = (
        (VODAFONE, 'Vodafone'),
        (AIRTEL, 'Airtel'),
        (MTN, 'MTN')
    )

    INIT = 'INIT'
    PAID = 'PAID'
    PROCESSED = 'PROC'
    CANCELLED = 'CANC'
    INVALID = 'INVD'

    TRANSACTION_STATES = (
        (INIT, 'initialized'),
        (PAID, 'paid'),
        (PROCESSED, 'processed'),
        (CANCELLED, 'cancelled'),
        (INVALID, 'invalid')
    )

    sender = models.ForeignKey(
        User,
        related_name='artime_topups',
        help_text='Sender associated with that topup'
    )

    exchange_rate = models.ForeignKey(
        ExchangeRate,
        related_name='airtime_topup',
        help_text='Exchange rate applied to this topup'
    )

    service_fee = models.ForeignKey(
        AirtimeServiceFee,
        related_name='airtime_topup',
        help_text='Service fee applied to this topup'
    )

    phone_number = models.CharField(
        'Mobile Money Phone Number',
        max_length=15,
        help_text='Phone number of recipient'
    )

    network = models.CharField(
        'Network',
        max_length=4,
        choices=NETWORK_CHOICES,
        help_text='Phone Network'
    )

    amount_ghs = models.FloatField(
        'Amount in GHS',
        help_text='Topup amount in GHS.'
    )

    reference_number = models.CharField(
        'Reference Number',
        max_length=6,
        help_text='6-digit reference number given to the customer to refer ' +
                  'to transaction in case of problems'
    )

    comments = models.TextField(
        'Comments',
        blank=True,
        help_text='Leave comments when manually solving problems with this transaction'
    )

    state = models.CharField(
        'State',
        max_length=4,
        choices=TRANSACTION_STATES,
        default=INIT,
        help_text='State of the transaction. ' +
                  'Init - Payment initiated. ' +
                  'Paid - Payment has been made. ' +
                  'Processed (manual) - Fulfillment completed by Beam. ' +
                  'Invalid - Error communicated by payment processor. ' +
                  'Cancelled (manual) - Cancelled by Beam'
    )

    initialized_at = models.DateTimeField(
        'Initialized at',
        auto_now_add=True,
        help_text='Time at which transaction was created by sender'
    )

    paid_at = models.DateTimeField(
        'Paid at',
        null=True,
        blank=True,
        help_text='Time at which payment was confirmed with payment gateway'
    )

    processed_at = models.DateTimeField(
        'Processed at',
        null=True,
        blank=True,
        help_text='Time at which equivalent amount was sent to customer'
    )

    cancelled_at = models.DateTimeField(
        'Cancelled at',
        null=True,
        blank=True,
        help_text='Time at which the transaction was cancelled and rolled back'
    )

    invalidated_at = models.DateTimeField(
        'Invalidated at',
        null=True,
        blank=True,
        help_text='Time at which payment was set invalid'
    )

    @property
    def charge_usd(self):
        return self.service_fee.fee + self.amount_ghs * self.exchange_rate.usd_ghs


class Transaction(models.Model):

    class Meta:
        ordering = ['-last_changed']

    # Constants
    INIT = 'INIT'
    GATHERING_INFO = 'INFO'
    PAID = 'PAID'
    PROCESSED = 'PROC'
    CANCELLED = 'CANC'
    INVALID = 'INVD'

    TRANSACTION_STATES = (
        (INIT, 'initialized'),
        (GATHERING_INFO, 'gatering information'),
        (PAID, 'paid'),
        (PROCESSED, 'processed'),
        (CANCELLED, 'cancelled'),
        (INVALID, 'invalid')
    )

    UTILITY_BILL = 'UTIL'
    GIFT = 'GIFT'
    SCHOOL_FEE = 'SCHL'
    HOSPITAL_BILL = 'HOSP'
    INTERNET = 'INTR'
    ERRAND = 'ERRD'
    OTHER = 'OTHR'

    TRANSACTION_TYPES = (
        (UTILITY_BILL, 'utility bill'),
        (GIFT, 'gift'),
        (SCHOOL_FEE, 'school fee'),
        (HOSPITAL_BILL, 'hospital bill'),
        (INTERNET, 'internet'),
        (ERRAND, 'errand'),
        (OTHER, 'other')
    )

    sender = models.ForeignKey(
        User,
        related_name='transactions',
        help_text='Sender associated with that transaction'
    )

    recipient = models.ForeignKey(
        Recipient,
        related_name='transactions',
        help_text='Recipient associated with that transaction'
    )

    transaction_type = models.CharField(
        'Type',
        max_length=4,
        choices=TRANSACTION_TYPES,
        default=OTHER,
        help_text='Categorization of service'
    )

    additional_info = models.CharField(
        'Additional Information',
        max_length=500,
        blank=True,
        help_text='Additional Information provided by user'
    )

    exchange_rate = models.ForeignKey(
        ExchangeRate,
        related_name='transaction',
        help_text='Exchange Rates applied to this transaction'
    )

    cost_of_delivery_usd = models.FloatField(
        'Cost of Delivery in USD',
        blank=True,
        null=True,
        help_text='Cost of the transaction in USD.'
    )

    cost_of_delivery_ghs = models.FloatField(
        'Cost of Delivery in GHS',
        blank=True,
        null=True,
        help_text='Cost of the transaction in GHS.'
    )

    service_charge = models.FloatField(
        'Service Charge in USD',
        blank=True,
        null=True,
        help_text='Service Charge of the transaction in USD'
    )

    reference_number = models.CharField(
        'Reference Number',
        max_length=6,
        help_text='6-digit reference number given to the customer to refer ' +
                  'to transaction in case of problems'
    )

    state = models.CharField(
        'State',
        max_length=4,
        choices=TRANSACTION_STATES,
        default=INIT,
        help_text='State of the transaction. ' +
                  'Init - Payment initiated. ' +
                  'Gathering Infromation - Additional Information required' +
                  'Paid - Payment has been made. ' +
                  'Processed (manual) - Fulfillment completed by Beam. ' +
                  'Invalid - Error communicated by payment processor. ' +
                  'Cancelled (manual) - Cancelled by Beam'
    )

    last_changed = models.DateTimeField(
        'Last changed',
        auto_now_add=True,
        help_text='Last changed'
    )

    def add_status_change(self, comment, author='user'):
        comment = Comment(
            transaction=self,
            author=author,
            comment=comment
        )

        comment.save()

    def save(self, *args, **kwargs):
        self.last_changed = timezone.now()
        super(Transaction, self).save(*args, **kwargs)


class Comment(models.Model):

    class Meta:
        ordering = ['-timestamp']

    transaction = models.ForeignKey(
        Transaction,
        related_name='comments',
        help_text='Transaction associated with comment.'
    )

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

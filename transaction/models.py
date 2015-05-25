import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from pricing.models import ExchangeRate

from recipient.models import Recipient


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

    def generate_reference_number(self):

        self.reference_number = str(random.randint(10000, 999999))

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

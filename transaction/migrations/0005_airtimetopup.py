# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_auto_20150526_2127'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0004_auto_20150526_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirtimeTopup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(help_text=b'Phone number of recipient', max_length=15, verbose_name=b'Mobile Money Phone Number')),
                ('network', models.CharField(help_text=b'Phone Network', max_length=4, verbose_name=b'Network', choices=[(b'VOD', b'Vodafone'), (b'AIR', b'Airtel'), (b'MTN', b'MTN')])),
                ('amount_ghs', models.FloatField(help_text=b'Topup amount in GHS.', verbose_name=b'Amount in GHS')),
                ('reference_number', models.CharField(help_text=b'6-digit reference number given to the customer to refer to transaction in case of problems', max_length=6, verbose_name=b'Reference Number')),
                ('comments', models.TextField(help_text=b'Leave comments when manually solving problems with this transaction', verbose_name=b'Comments', blank=True)),
                ('state', models.CharField(default=b'INIT', help_text=b'State of the transaction. Init - Payment initiated. Paid - Payment has been made. Processed (manual) - Fulfillment completed by Beam. Invalid - Error communicated by payment processor. Cancelled (manual) - Cancelled by Beam', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'INVD', b'invalid')])),
                ('initialized_at', models.DateTimeField(help_text=b'Time at which transaction was created by sender', verbose_name=b'Initialized at', auto_now_add=True)),
                ('paid_at', models.DateTimeField(help_text=b'Time at which payment was confirmed with payment gateway', null=True, verbose_name=b'Paid at', blank=True)),
                ('processed_at', models.DateTimeField(help_text=b'Time at which equivalent amount was sent to customer', null=True, verbose_name=b'Processed at', blank=True)),
                ('cancelled_at', models.DateTimeField(help_text=b'Time at which the transaction was cancelled and rolled back', null=True, verbose_name=b'Cancelled at', blank=True)),
                ('invalidated_at', models.DateTimeField(help_text=b'Time at which payment was set invalid', null=True, verbose_name=b'Invalidated at', blank=True)),
                ('exchange_rate', models.ForeignKey(related_name='airtime_topup', to='pricing.ExchangeRate', help_text=b'Exchange rate applied to this topup')),
                ('sender', models.ForeignKey(related_name='artime_topups', to=settings.AUTH_USER_MODEL, help_text=b'Sender associated with that topup')),
                ('service_fee', models.ForeignKey(related_name='airtime_topup', to='pricing.AirtimeServiceFee', help_text=b'Service fee applied to this topup')),
            ],
            options={
                'ordering': ['-initialized_at'],
            },
            bases=(models.Model,),
        ),
    ]

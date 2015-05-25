# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
        ('recipient', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(help_text=b'Author of comment', max_length=50, verbose_name=b'Author')),
                ('timestamp', models.DateTimeField(help_text=b'Timestamp of comment', verbose_name=b'Timestamp', auto_now_add=True)),
                ('comment', models.CharField(help_text=b'The comment itself', max_length=300, verbose_name=b'Comment')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_of_delivery_usd', models.FloatField(help_text=b'Cost of the .', verbose_name=b'Cost of Delivery in USD', blank=True)),
                ('cost_of_delivery_ghs', models.FloatField(help_text=b'Cost of the .', verbose_name=b'Cost of Delivery in GHS', blank=True)),
                ('service_charge', models.FloatField(help_text=b'Service Charge in USD for the transaction', verbose_name=b'Service Charge in USD', blank=True)),
                ('reference_number', models.CharField(help_text=b'6-digit reference number given to the customer to refer to transaction in case of problems', max_length=6, verbose_name=b'Reference Number')),
                ('state', models.CharField(default=b'INIT', help_text=b'State of the transaction. Init - Payment initiated. Gathering Infromation - Additional Information requiredPaid - Payment has been made. Processed (manual) - Fulfillment completed by Beam. Invalid - Error communicated by payment processor. Cancelled (manual) - Cancelled by Beam', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'INVD', b'invalid')])),
                ('last_changed', models.DateTimeField(help_text=b'Last changed', verbose_name=b'Last changed', auto_now_add=True)),
                ('exchange_rate', models.ForeignKey(related_name='transaction', to='pricing.ExchangeRate', help_text=b'Exchange Rates applied to this transaction')),
                ('recipient', models.ForeignKey(related_name='transactions', to='recipient.Recipient', help_text=b'Recipient associated with that transaction')),
                ('sender', models.ForeignKey(related_name='transactions', to=settings.AUTH_USER_MODEL, help_text=b'Sender associated with that transaction')),
            ],
            options={
                'ordering': ['-last_changed'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='transaction',
            field=models.ForeignKey(related_name='comments', to='transaction.Transaction', help_text=b'Transaction associated with comment.'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cost_of_delivery_ghs',
            field=models.FloatField(help_text=b'Cost of the transaction in GHS.', null=True, verbose_name=b'Cost of Delivery in GHS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cost_of_delivery_usd',
            field=models.FloatField(help_text=b'Cost of the transaction in USD.', null=True, verbose_name=b'Cost of Delivery in USD'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference_number',
            field=models.CharField(default=b'735323', help_text=b'6-digit reference number given to the customer to refer to transaction in case of problems', max_length=6, verbose_name=b'Reference Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='service_charge',
            field=models.FloatField(help_text=b'Service Charge of the transaction in USD', null=True, verbose_name=b'Service Charge in USD'),
            preserve_default=True,
        ),
    ]

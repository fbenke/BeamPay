# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0019_auto_20150627_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtimetopup',
            name='remarks',
            field=models.TextField(help_text=b'Remarks about fulfillment of the transaction,                   not to be displayed to customer.', verbose_name=b'Remarks', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billpayment',
            name='remarks',
            field=models.TextField(help_text=b'Remarks about fulfillment of the transaction,                   not to be displayed to customer.', verbose_name=b'Remarks', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gift',
            name='remarks',
            field=models.TextField(help_text=b'Remarks about fulfillment of the transaction,                   not to be displayed to customer.', verbose_name=b'Remarks', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schoolfeepayment',
            name='remarks',
            field=models.TextField(help_text=b'Remarks about fulfillment of the transaction,                   not to be displayed to customer.', verbose_name=b'Remarks', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='valettransaction',
            name='remarks',
            field=models.TextField(help_text=b'Remarks about fulfillment of the transaction,                   not to be displayed to customer.', verbose_name=b'Remarks', blank=True),
            preserve_default=True,
        ),
    ]

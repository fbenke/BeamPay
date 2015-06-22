# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_billpayment_gift_schoolfeepayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gift',
            old_name='bill_type',
            new_name='gift_type',
        ),
        migrations.AlterField(
            model_name='gift',
            name='additional_info',
            field=models.TextField(help_text=b'Anything else we should know, e.g.         occasion, special requests.', max_length=500, verbose_name=b'Additional information', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='delivery_address',
            field=models.TextField(help_text=b'Delivery address', max_length=500, verbose_name=b'Delivery address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schoolfeepayment',
            name='additional_info',
            field=models.TextField(help_text=b'Anything else required to know about        the payment, e.g. hall, class, student id', max_length=500, verbose_name=b'Additional information', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='valettransaction',
            name='description',
            field=models.TextField(help_text=b'Description of the valet request', max_length=500, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
    ]

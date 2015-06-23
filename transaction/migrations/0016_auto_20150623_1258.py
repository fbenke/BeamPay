# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0015_billpayment_service_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valettransaction',
            name='description',
            field=models.TextField(help_text=b'Description of the valet request', max_length=500, verbose_name=b'Description'),
            preserve_default=True,
        ),
    ]

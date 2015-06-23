# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0004_delete_airtimeservicefee'),
        ('transaction', '0014_auto_20150622_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='billpayment',
            name='service_fee',
            field=models.ForeignKey(related_name='bill_payment', default=1, to='pricing.ServiceFee', help_text=b'Service fee applied to this bill payment'),
            preserve_default=False,
        ),
    ]

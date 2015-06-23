# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0003_servicefee'),
        ('transaction', '0013_auto_20150622_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airtimetopup',
            name='airtime_service_fee',
        ),
        migrations.AddField(
            model_name='airtimetopup',
            name='service_fee',
            field=models.ForeignKey(related_name='airtime_topup', default=0, to='pricing.ServiceFee', help_text=b'Service fee applied to this topup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='billpayment',
            name='reference',
            field=models.CharField(help_text=b'Reference for bill payment', max_length=20, verbose_name=b'Optional reference', blank=True),
            preserve_default=True,
        ),
    ]

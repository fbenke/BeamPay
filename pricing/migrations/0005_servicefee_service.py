# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0004_delete_airtimeservicefee'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicefee',
            name='service',
            field=models.CharField(default=b'AIRTIME', help_text=b'The service which the fee is for.', max_length=10, verbose_name=b'Service', choices=[(b'AIRTIME', b'AIRTIME'), (b'BILL', b'BILL')]),
            preserve_default=True,
        ),
    ]

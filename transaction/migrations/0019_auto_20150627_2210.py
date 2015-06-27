# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0018_airtimetopup_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billpayment',
            name='bill_type',
            field=models.CharField(help_text=b'Type of bill', max_length=3, verbose_name=b'Type of bill', choices=[(b'ECG', b'ECG (electricity)'), (b'GWC', b'GWC (water)'), (b'DST', b'DStv'), (b'GOT', b'GOtv'), (b'SRF', b'surfline'), (b'VOB', b'Vodafone Broadband')]),
            preserve_default=True,
        ),
    ]

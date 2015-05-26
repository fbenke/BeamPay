# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20150525_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='additional_info',
            field=models.CharField(help_text=b'Additional Information provided by user', max_length=500, verbose_name=b'Additional Information', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(default=b'OTHR', help_text=b'Categorization of service', max_length=4, verbose_name=b'Type', choices=[(b'UTIL', b'utility bill'), (b'GIFT', b'gift'), (b'SCHL', b'school fee'), (b'HOSP', b'hospital bill'), (b'INTR', b'internet'), (b'ERRD', b'errand'), (b'OTHR', b'other')]),
            preserve_default=True,
        ),
    ]

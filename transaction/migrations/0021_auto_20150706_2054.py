# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0020_auto_20150705_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='delivery_time',
            field=models.DateTimeField(help_text=b'Delivery date and time', null=True, verbose_name=b'Delivery date and time', blank=True),
            preserve_default=True,
        ),
    ]

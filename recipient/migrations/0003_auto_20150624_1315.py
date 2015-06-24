# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0002_auto_20150524_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='phone_number',
            field=models.CharField(help_text=b'Phone number of recipient', max_length=15, verbose_name=b'Phone Number'),
            preserve_default=True,
        ),
    ]

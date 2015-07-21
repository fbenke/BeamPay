# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20150710_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='beamprofile',
            name='trusted',
            field=models.BooleanField(default=False, help_text=b'Trusted because we know that person or verified that person', verbose_name=b'Trusted User'),
            preserve_default=True,
        ),
    ]

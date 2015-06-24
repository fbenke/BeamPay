# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0017_auto_20150623_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtimetopup',
            name='phone_number',
            field=models.CharField(default='01234', help_text=b'Phone number of recipient', max_length=15, verbose_name=b'Phone Number'),
            preserve_default=False,
        ),
    ]

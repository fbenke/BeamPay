# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150311_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='beamprofile',
            name='facebook_link',
            field=models.CharField(help_text=b'Link to Facebook Profile', max_length=100, verbose_name=b'Facebook Link', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='gender',
            field=models.CharField(help_text=b'Gender', max_length=15, verbose_name=b'Gender', blank=True),
            preserve_default=True,
        ),
    ]

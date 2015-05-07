# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150326_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='beamprofile',
            name='city',
            field=models.CharField(help_text=b'City', max_length=40, verbose_name=b'City', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='post_code',
            field=models.CharField(help_text=b'Post Code', max_length=50, verbose_name=b'Post Code', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='street',
            field=models.CharField(help_text=b'Street and number', max_length=50, verbose_name=b'Street and number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beamprofile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, blank=True, help_text=b'Country of Current Residence', null=True, verbose_name=b'Country'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beamprofile',
            name='phone_number',
            field=models.CharField(help_text=b'Phone number', max_length=15, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beamprofile',
            name='date_of_birth',
            field=models.DateField(help_text=b'Date of birth', null=True, verbose_name=b'Date of Birth', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='phone_number',
            field=models.CharField(help_text=b'Phone number', max_length=15, verbose_name=b'Mobile Money Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beamprofile',
            name='accepted_privacy_policy',
            field=models.BooleanField(default=True, verbose_name=b'Privacy policy accepted'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beamprofile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, blank=True, help_text=b'Country', null=True, verbose_name=b'Country'),
            preserve_default=True,
        ),
    ]

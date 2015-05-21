# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(help_text=b'Time at which exchange rate came into effect.', verbose_name=b'Start Time', auto_now_add=True)),
                ('end', models.DateTimeField(help_text=b'Time at which exchange rate came ended. If null, it represents the current exchange rate.Only one row in this table can have a null value for this column.', null=True, verbose_name=b'End Time', blank=True)),
                ('usd_ghs', models.FloatField(help_text=b'Exchange Rate from USD to GHS without markup', verbose_name=b'USD to GHS Exchange Rate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirtimeServiceFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(help_text=b'Time at which pricing structure came into effect', verbose_name=b'Start Time', auto_now_add=True)),
                ('end', models.DateTimeField(help_text=b'Time at which pricing ended.', null=True, verbose_name=b'End Time', blank=True)),
                ('fee', models.FloatField(help_text=b'Service fee charged for the airtime topup.', verbose_name=b'Service Fee in USD')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='end',
            field=models.DateTimeField(help_text=b'Time at which exchange rate came ended.', null=True, verbose_name=b'End Time', blank=True),
            preserve_default=True,
        ),
    ]

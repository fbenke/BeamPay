# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_auto_20150526_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(help_text=b'Time at which pricing structure came into effect', verbose_name=b'Start Time', auto_now_add=True)),
                ('end', models.DateTimeField(help_text=b'Time at which pricing ended.', null=True, verbose_name=b'End Time', blank=True)),
                ('fixed_fee', models.FloatField(help_text=b'Service fee charged for the airtime topup.', verbose_name=b'Service fee in USD')),
                ('percentual_fee', models.FloatField(help_text=b'Percentual amount to be added as charge.        Value between 0 and 1.', verbose_name=b'Percentual fee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

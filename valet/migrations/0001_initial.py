# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsappRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wap_number', models.CharField(help_text=b'WhatsApp number sent as a request', max_length=23, verbose_name=b'WhatsApp Number')),
                ('handler', models.CharField(default=b'0', help_text=b'Beam Crew member handling the request', max_length=1, verbose_name=b'Handler')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

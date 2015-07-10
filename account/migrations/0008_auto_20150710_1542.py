# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20150618_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beamprofile',
            options={'ordering': ['-user_id']},
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='preferred_contact_details',
            field=models.CharField(help_text=b'Preferred Contact Details', max_length=20, verbose_name=b'Preferred Contact Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beamprofile',
            name='phone_number',
            field=models.CharField(help_text=b'Phone number', max_length=20, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_beamprofile_trusted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamprofile',
            name='preferred_contact_details',
            field=models.CharField(help_text=b'Preferred Contact Details', max_length=254, verbose_name=b'Preferred Contact Details', blank=True),
            preserve_default=True,
        ),
    ]

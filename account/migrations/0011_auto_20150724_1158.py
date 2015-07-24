# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20150723_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beamprofile',
            name='trusted',
        ),
        migrations.AddField(
            model_name='beamprofile',
            name='trust_status',
            field=models.CharField(default=b'NEUT', help_text=b'Trusted because we know that person or verified that person', max_length=4, verbose_name=b'Trusted User', choices=[(b'TRST', b'Trusted'), (b'FRAD', b'Fraudulent'), (b'NEUT', b'Neutral')]),
            preserve_default=True,
        ),
    ]

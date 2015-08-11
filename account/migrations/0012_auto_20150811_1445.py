# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20150724_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamprofile',
            name='trust_status',
            field=models.CharField(default=b'NEUT', help_text=b'Additional information on trustworthiness of this account', max_length=4, verbose_name=b'Trustworthiness', choices=[(b'TRST', b'Trusted'), (b'FRAD', b'Fraudulent'), (b'NEUT', b'Neutral')]),
            preserve_default=True,
        ),
    ]

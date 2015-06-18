# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150526_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamprofile',
            name='preferred_contact_method',
            field=models.CharField(default=b'PHON', help_text=b'Preferred Contact Method', max_length=4, verbose_name=b'Preferred Contact Method', choices=[(b'PHON', b'phone call'), (b'MAIL', b'email'), (b'SMS', b'sms'), (b'WAP', b'whatsapp')]),
            preserve_default=True,
        ),
    ]

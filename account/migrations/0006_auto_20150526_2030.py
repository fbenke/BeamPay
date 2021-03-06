# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_beamprofile_preferred_contact_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamprofile',
            name='preferred_contact_method',
            field=models.CharField(default=b'PHON', help_text=b'Preferred Contact Method', max_length=4, verbose_name=b'Preferred Contact Method', choices=[(b'PHON', b'phone call'), (b'MAIL', b'email'), (b'SMS', b'sms')]),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsapprequest',
            name='handler',
            field=models.CharField(default=b'0', help_text=b'Beam Crew member handling the request', max_length=1, verbose_name=b'Handler', choices=[(b'0', b'No one'), (b'1', b'Kingston'), (b'2', b'Falk'), (b'3', b'Gerald')]),
            preserve_default=True,
        ),
    ]

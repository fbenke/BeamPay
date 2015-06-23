# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0016_auto_20150623_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolfeepayment',
            name='school',
            field=models.CharField(help_text=b'Name of school or university', max_length=100, verbose_name=b'Name of school'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schoolfeepayment',
            name='ward_name',
            field=models.CharField(help_text=b'Name of ward', max_length=100, verbose_name=b'Name of ward or student'),
            preserve_default=True,
        ),
    ]

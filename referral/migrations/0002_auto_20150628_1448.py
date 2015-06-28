# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='referred',
        ),
        migrations.AddField(
            model_name='referral',
            name='referred_by',
            field=models.ForeignKey(to='referral.Referral', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='referral',
            name='referred_to',
            field=models.ManyToManyField(related_name='referer', null=True, to='referral.Referral'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referral',
            name='code',
            field=models.CharField(help_text=b'Referral code', unique=True, max_length=50, verbose_name=b'Referral code'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0002_auto_20150628_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='credits_redeemed',
            field=models.IntegerField(default=0, help_text=b'How many of the credits have been redeemed?', verbose_name=b'Credits redeemed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referral',
            name='user',
            field=models.OneToOneField(related_name='referral', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

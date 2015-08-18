# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0022_auto_20150811_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtimetopup',
            name='free_from_referral',
            field=models.BooleanField(default=False, help_text=b'Whether the transaction was free based on referral', verbose_name=b'Is free from referrals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billpayment',
            name='free_from_referral',
            field=models.BooleanField(default=False, help_text=b'Whether the transaction was free based on referral', verbose_name=b'Is free from referrals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gift',
            name='free_from_referral',
            field=models.BooleanField(default=False, help_text=b'Whether the transaction was free based on referral', verbose_name=b'Is free from referrals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schoolfeepayment',
            name='free_from_referral',
            field=models.BooleanField(default=False, help_text=b'Whether the transaction was free based on referral', verbose_name=b'Is free from referrals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='valettransaction',
            name='free_from_referral',
            field=models.BooleanField(default=False, help_text=b'Whether the transaction was free based on referral', verbose_name=b'Is free from referrals'),
            preserve_default=True,
        ),
    ]

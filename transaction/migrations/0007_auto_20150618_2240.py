# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0002_auto_20150524_2158'),
        ('transaction', '0006_auto_20150528_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airtimetopup',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='airtimetopup',
            name='recipient',
            field=models.ForeignKey(related_name='airtime_topups', default=1, to='recipient.Recipient', help_text=b'Recipient associated with that transaction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='airtimetopup',
            name='network',
            field=models.CharField(help_text=b'Phone Network', max_length=4, verbose_name=b'Network', choices=[(b'VOD', b'Vodafone'), (b'AIR', b'Airtel'), (b'MTN', b'MTN'), (b'TIG', b'Tigo')]),
            preserve_default=True,
        ),
    ]

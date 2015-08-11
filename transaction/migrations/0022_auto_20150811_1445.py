# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0021_auto_20150706_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airtimetopup',
            name='state',
            field=models.CharField(default=b'INIT', help_text=b'State of the transaction.', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'REDY', b'ready for payment'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'FRUD', b'fraudulent'), (b'INVD', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='billpayment',
            name='state',
            field=models.CharField(default=b'INIT', help_text=b'State of the transaction.', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'REDY', b'ready for payment'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'FRUD', b'fraudulent'), (b'INVD', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='state',
            field=models.CharField(default=b'INIT', help_text=b'State of the transaction.', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'REDY', b'ready for payment'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'FRUD', b'fraudulent'), (b'INVD', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schoolfeepayment',
            name='state',
            field=models.CharField(default=b'INIT', help_text=b'State of the transaction.', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'REDY', b'ready for payment'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'FRUD', b'fraudulent'), (b'INVD', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='valettransaction',
            name='state',
            field=models.CharField(default=b'INIT', help_text=b'State of the transaction.', max_length=4, verbose_name=b'State', choices=[(b'INIT', b'initialized'), (b'INFO', b'gatering information'), (b'REDY', b'ready for payment'), (b'PAID', b'paid'), (b'PROC', b'processed'), (b'CANC', b'cancelled'), (b'FRUD', b'fraudulent'), (b'INVD', b'invalid')]),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_auto_20150620_2156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airtimetopup',
            old_name='cost_of_transaction_ghs',
            new_name='amount_ghs',
        ),
        migrations.RenameField(
            model_name='airtimetopup',
            old_name='cost_of_transaction_usd',
            new_name='amount_usd',
        ),
        migrations.RenameField(
            model_name='valettransaction',
            old_name='cost_of_transaction_ghs',
            new_name='amount_ghs',
        ),
        migrations.RenameField(
            model_name='valettransaction',
            old_name='cost_of_transaction_usd',
            new_name='amount_usd',
        ),
    ]

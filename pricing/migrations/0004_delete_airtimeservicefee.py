# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0014_auto_20150622_2333'),
        ('pricing', '0003_servicefee'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AirtimeServiceFee',
        ),
    ]

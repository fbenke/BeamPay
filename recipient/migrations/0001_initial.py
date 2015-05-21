# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(help_text=b'First name of recipient', max_length=50, verbose_name=b'First Name')),
                ('last_name', models.CharField(help_text=b'Last name of recipient', max_length=50, verbose_name=b'Full Name')),
                ('phone_number', models.CharField(help_text=b'Phone number of recipient', max_length=15, verbose_name=b'Mobile Money Phone Number')),
                ('email', models.EmailField(help_text=b'Email of recipient', max_length=75, verbose_name=b'Email', blank=True)),
                ('date_of_birth', models.DateField(help_text=b'Date of birth', null=True, verbose_name=b'Date of Birth', blank=True)),
                ('relation', models.CharField(default=b'USP', help_text=b'Relation between user and recipient', max_length=3, verbose_name=b'Relation between user and recipients', choices=[(b'PAR', b'parent'), (b'SIB', b'sibling'), (b'FRD', b'friend'), (b'USP', b'not provided')])),
                ('user', models.ForeignKey(related_name='recipients', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

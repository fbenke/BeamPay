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
            name='Referral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Referral code', max_length=50, verbose_name=b'Referral code')),
                ('credits_gained', models.IntegerField(default=0, help_text=b'How many credits did the user gain through referrals?', verbose_name=b'Credits gained')),
                ('credits_redeemed', models.IntegerField(default=0, help_text=b'How often has this code been redeemed?', verbose_name=b'Credits redeemed')),
                ('referred', models.ManyToManyField(related_name='referred_rel_+', null=True, to='referral.Referral')),
                ('user', models.OneToOneField(related_name='referral', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

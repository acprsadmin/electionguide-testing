# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0026_auto_20200531_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='early_voting_instructions',
            field=models.TextField(null=True, verbose_name=b'Early Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_instructions',
            field=models.TextField(null=True, verbose_name=b'Mail Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_instructions',
            field=models.TextField(null=True, verbose_name=b'Online Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0012_auto_20200427_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='primary_voting_method',
            field=models.IntegerField(null=True, verbose_name=b'Primary Voting Method by', blank=True),
            preserve_default=True,
        ),
    ]

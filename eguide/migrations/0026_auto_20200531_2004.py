# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0025_auto_20200513_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_instructions',
            field=models.TextField(null=True, verbose_name=b'In Person Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
    ]

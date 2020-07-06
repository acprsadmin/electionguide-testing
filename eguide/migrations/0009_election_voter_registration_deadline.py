# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0008_auto_20200408_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='voter_registration_deadline',
            field=models.DateField(null=True, verbose_name=b'Voter Registration Deadline', blank=True),
            preserve_default=True,
        ),
    ]

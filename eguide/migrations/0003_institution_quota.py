# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0002_auto_20150205_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='quota',
            field=models.CharField(help_text=b'e.g. Yes: "Legislated Candidate Quotas" in the National Constituent Assembly', max_length=350, null=True, verbose_name=b'Gender Quota', blank=True),
            preserve_default=True,
        ),
    ]

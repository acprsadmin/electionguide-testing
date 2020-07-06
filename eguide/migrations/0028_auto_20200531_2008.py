# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0027_auto_20200531_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
    ]

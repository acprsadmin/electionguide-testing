# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0019_auto_20200511_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='api_access_date',
            field=models.DateTimeField(help_text=b'', null=True, verbose_name=b'Last Facebook Download Date', blank=True),
            preserve_default=True,
        ),
    ]

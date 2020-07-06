# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0014_auto_20200430_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='early_voting_isprimary',
        ),
        migrations.RemoveField(
            model_name='election',
            name='inperson_voting_isprimary',
        ),
        migrations.RemoveField(
            model_name='election',
            name='mail_voting_isprimary',
        ),
        migrations.RemoveField(
            model_name='election',
            name='online_voting_isprimary',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0024_auto_20200513_1714'),
    ]

    operations = [
    	migrations.RenameField('Election', 'oneline_voting_end_time', 'online_voting_end_time'),
    ]

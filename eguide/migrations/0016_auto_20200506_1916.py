# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0015_auto_20200430_1954'),
    ]

    operations = [
      migrations.AlterField('election', 'inperson_voting_start',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'early_voting_start',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'mail_voting_start',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'online_voting_start',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'inperson_voting_end',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'early_voting_end',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'mail_voting_end',  models.DateTimeField(null=True, blank=True)),
      migrations.AlterField('election', 'online_voting_end',  models.DateTimeField(null=True, blank=True)),
    ]

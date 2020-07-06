# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0013_election_primary_voting_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='primary_voting_method',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Primary Voting Method', choices=[(1, b'In Person Voting'), (2, b'Early Voting'), (3, b'By Mail Voting'), (4, b'Online Voting')]),
            preserve_default=True,
        ),
    ]

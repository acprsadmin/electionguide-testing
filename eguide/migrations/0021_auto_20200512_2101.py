# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0020_election_api_access_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='yn_early_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Early Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='yn_inperson_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'In Person Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='yn_mail_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Mail Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
    ]

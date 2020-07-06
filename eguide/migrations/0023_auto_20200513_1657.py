# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0022_auto_20200513_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='early_voting_end',
            field=models.DateField(null=True, verbose_name=b'Early Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='early_voting_start',
            field=models.DateField(null=True, verbose_name=b'Early Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_blackout_end_date',
            field=models.DateField(null=True, verbose_name=b'Blackout Date End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_blackout_start_date',
            field=models.DateField(null=True, verbose_name=b'Blackout Date Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_candidate_filing_deadline',
            field=models.DateField(null=True, verbose_name=b'Candidate Filing  Deadline', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_end',
            field=models.DateField(null=True, verbose_name=b'In Person Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_start',
            field=models.DateField(null=True, verbose_name=b'In Person Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_end',
            field=models.DateField(null=True, verbose_name=b'Mail Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_start',
            field=models.DateField(null=True, verbose_name=b'Mail Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_end',
            field=models.DateField(null=True, verbose_name=b'Online Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_start',
            field=models.DateField(null=True, verbose_name=b'Online Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='voter_registration_deadline',
            field=models.DateField(null=True, verbose_name=b'Voter Registration Deadline', blank=True),
            preserve_default=True,
        ),
    ]

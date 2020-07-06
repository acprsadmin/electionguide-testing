# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0023_auto_20200513_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='early_voting_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Early Voting End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Early Voting Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_blackout_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Blackout End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_blackout_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Blackout  Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_candidate_filing_deadline_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Candidate Filing  Deadline Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_declared_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Declared End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_declared_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Declared Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'In Person Voting End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'In Person Voting Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Mail Voting End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Mail Voting Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='oneline_voting_end_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Early Voting End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_start_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Early Voting  Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='voter_registration_deadline_time',
            field=models.TimeField(help_text=b'Optional', null=True, verbose_name=b'Voter Registration Deadline Time', blank=True),
            preserve_default=True,
        ),
    ]

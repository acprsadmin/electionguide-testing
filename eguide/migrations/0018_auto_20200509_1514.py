# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0017_auto_20200508_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='election_candidate_filing_deadline_notes',
            field=models.TextField(verbose_name=b'Candidate Filing Deadline Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_range_notes',
            field=models.TextField(verbose_name=b'Election Date Range Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='published_by_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Person  Name publisher', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='submitted_by_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Person Name submitting for publication', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='blackout_date_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Blackout Date Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='cso_confirmation',
            field=models.BooleanField(default=False, help_text=b'Check if confirmed', verbose_name=b'CSO Confirmation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_details',
            field=models.TextField(null=True, verbose_name=b'Disinforamtion Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_prohibition_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Disinformation Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_blackout_end_date',
            field=models.DateTimeField(null=True, verbose_name=b'Blackout Date End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_blackout_start_date',
            field=models.DateTimeField(null=True, verbose_name=b'Blackout Date Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_candidate_filing_deadline',
            field=models.DateTimeField(null=True, verbose_name=b'Candidate Filing  Deadline', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_declared_start_date',
            field=models.DateTimeField(help_text=b'', null=True, verbose_name=b'Election Declared Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_rights_info_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Electoral Rights Info Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_system_other',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Electoral system notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_system_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Electoral System Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_confirmation',
            field=models.BooleanField(default=False, help_text=b'Check if confirmed', verbose_name=b'EMB Confirmation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_details',
            field=models.TextField(null=True, verbose_name=b'Hate Speech Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_prohibition_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Hate Speech Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='ifes_confirmation',
            field=models.BooleanField(default=False, help_text=b'Check if confirmed', verbose_name=b'IFES Confirmation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='is_delayed_covid19',
            field=models.BooleanField(default=False, help_text=b'Check if true', verbose_name=b'Election Delayed by Covid-19'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='is_national_exec',
            field=models.BooleanField(default=False, help_text=b'Check if applicable', verbose_name=b'NATIONAL_EXEC'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='is_national_legislative',
            field=models.BooleanField(default=False, help_text=b'Check if applicable', verbose_name=b'NATIONAL_LEGISLATIVE'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='is_national_lower',
            field=models.BooleanField(default=False, help_text=b'Check if applicable', verbose_name=b'NATIONAL_LOWER'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='is_national_upper',
            field=models.BooleanField(default=False, help_text=b'Check if applicable', verbose_name=b'NATIONAL_UPPER'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='legal_consultant_confirmation',
            field=models.BooleanField(default=False, help_text=b'Check if confirmed', verbose_name=b'Legal Consultant Confirmation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='restrict_electoral_rights',
            field=models.BooleanField(default=False, help_text=b'Check if true', verbose_name=b'Restrict Electoral Rights?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='restrict_electoral_rights_details',
            field=models.TextField(null=True, verbose_name=b'Restrict Electoral Rights Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='support_electoral_rights',
            field=models.BooleanField(default=False, help_text=b'Check if true', verbose_name=b'Support Electoral Rights?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='support_electoral_rights_details',
            field=models.TextField(null=True, verbose_name=b'Support Electoral Rights Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='voter_registration_deadline',
            field=models.DateTimeField(null=True, verbose_name=b'Voter Registration Deadline', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='voting_age_minimum_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Voting Age Minimum Source', blank=True),
            preserve_default=True,
        ),
    ]

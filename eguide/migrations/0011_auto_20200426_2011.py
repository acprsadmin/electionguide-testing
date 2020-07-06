# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0010_auto_20200408_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election_Demo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name=b'Enabled?')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='election',
            name='is_delayed_covid19',
            field=models.BooleanField(default=False, verbose_name=b'Election Delayed by Covid-19'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='original_election_year',
            field=models.IntegerField(help_text=b'Original Year of the Election', null=True, verbose_name=b'Original Election Year', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='administering_election_commission_website',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election Commission Website', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='blackout_date_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Blackout Date Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='cso_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'CSO Confirmation Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Disinforamtion Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_prohibition',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Disinformation Prohibited?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_prohibition_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Disinformation Prohibition Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_candidate_filing_deadline_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Candidate Filing Deadline Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_declared_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election declared date source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_range_source',
            field=models.CharField(help_text=b'', max_length=250, null=True, verbose_name=b'Range Date Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='election_scope',
            field=models.ForeignKey(default=1, blank=True, to='eguide.Election_scope', help_text=b'*NEW*', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_rights_info_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral Rights Info Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_system_other',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral system notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='electoral_system_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral System Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Embassy Confirmation Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Hate Speech Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_prohibition',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Hate Speech Prohibited?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_prohibition_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Hate Speech Prohibition Source', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='ifes_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'IFES Confirmation Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='legal_consultant_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Legal Consultant Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='restrict_electoral_rights_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Restrict Electoral Rights Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='source_website',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election Website', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='support_electoral_rights_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Support Electoral Rights Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='voting_age_minimum_inclusive',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Voting Age Minimum', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='voting_age_minimum_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Voting Age Minimum Source', blank=True),
            preserve_default=True,
        ),
    ]

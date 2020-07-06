# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0004_auto_20150302_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election_scope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name=b'Enabled?')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text=b'', max_length=400, verbose_name=b'Election Scope Name')),
            ],
            options={
                'verbose_name': 'Election Scope',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Electoral_system',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name=b'Enabled?')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text=b'', max_length=400, verbose_name=b'Electoral System Name')),
            ],
            options={
                'verbose_name': 'Electoral System',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='election',
            name='administering_election_commission_website',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election Commission Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='blackout_date_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Blackout Date Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_blackout_end_date',
            field=models.DateField(null=True, verbose_name=b'Blackout Date End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_blackout_start_date',
            field=models.DateField(null=True, verbose_name=b'Blackout Date Start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_candidate_filing_deadline',
            field=models.DateField(null=True, verbose_name=b'Candidate Filing  Deadline', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_candidate_filing_deadline_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Candidate Filing Deadline Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_declared_end_date',
            field=models.DateField(help_text=b'', null=True, verbose_name=b'Election Declared End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_declared_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election declared date source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_declared_start_date',
            field=models.DateField(help_text=b'', null=True, verbose_name=b'Election Declared Start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_range_end_date',
            field=models.DateField(help_text=b'', null=True, verbose_name=b'Election Range End Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_range_source',
            field=models.CharField(help_text=b'', max_length=250, null=True, verbose_name=b'Range Date Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='election_range_start_date',
            field=models.DateField(help_text=b'', null=True, verbose_name=b'Election Range Start Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='electoral_system',
            field=models.ForeignKey(blank=True, to='eguide.Electoral_system', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='electoral_system_other',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral system notes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='electoral_system_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral System Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='source_website',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Election Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='voting_age_minimum_inclusive',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Voting Age Minimum'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='voting_age_minimum_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Voting Age Minimum Source'),
            preserve_default=True,
        ),
    ]

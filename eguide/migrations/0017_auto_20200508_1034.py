# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0016_auto_20200506_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='early_voting_enabled',
            field=models.BooleanField(default=False, help_text=b'Check this to publish method to FB json', verbose_name=b'Early Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='early_voting_end',
            field=models.DateTimeField(null=True, verbose_name=b'Early Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='early_voting_start',
            field=models.DateTimeField(null=True, verbose_name=b'Early Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_comments',
            field=models.TextField(verbose_name=b'EMB Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_confirmation',
            field=models.BooleanField(default=False, verbose_name=b'EMB Confirmation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_confirmation_date',
            field=models.DateField(null=True, verbose_name=b'EMB Confirmation Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='embassy_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'EMB Confirmation Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_enabled',
            field=models.BooleanField(default=False, help_text=b'Check this to publish method to FB json', verbose_name=b'In Person Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_end',
            field=models.DateTimeField(null=True, verbose_name=b'In Person Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='inperson_voting_start',
            field=models.DateTimeField(null=True, verbose_name=b'In Person Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_enabled',
            field=models.BooleanField(default=False, help_text=b'Check this to publish method to FB json', verbose_name=b'Mail Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_end',
            field=models.DateTimeField(null=True, verbose_name=b'Mail Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='mail_voting_start',
            field=models.DateTimeField(null=True, verbose_name=b'Mail Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_enabled',
            field=models.BooleanField(default=False, help_text=b'Check this to publish method to FB json', verbose_name=b'Online Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_end',
            field=models.DateTimeField(null=True, verbose_name=b'Online Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='online_voting_start',
            field=models.DateTimeField(null=True, verbose_name=b'Online Voting Method Start', blank=True),
            preserve_default=True,
        ),
    ]

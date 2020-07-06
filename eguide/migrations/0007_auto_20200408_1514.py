# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0006_auto_20200408_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='early_voting_enabled',
            field=models.BooleanField(default=False, verbose_name=b'Early Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_end',
            field=models.DateField(null=True, verbose_name=b'Early Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_excuse_required',
            field=models.BooleanField(default=False, verbose_name=b'Early Voting Method Excuse Required?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_instructions',
            field=models.TextField(verbose_name=b'Early Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_isprimary',
            field=models.BooleanField(default=False, verbose_name=b'Early Voting Primary Method?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='early_voting_start',
            field=models.DateField(null=True, verbose_name=b'Early Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_enabled',
            field=models.BooleanField(default=False, verbose_name=b'In Person Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_end',
            field=models.DateField(null=True, verbose_name=b'In Person Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_excuse_required',
            field=models.BooleanField(default=False, verbose_name=b'In Person Voting Method Excuse Required?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_instructions',
            field=models.TextField(verbose_name=b'In Person Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_isprimary',
            field=models.BooleanField(default=False, verbose_name=b'In Person Primary Method?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='inperson_voting_start',
            field=models.DateField(null=True, verbose_name=b'In Person Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_enabled',
            field=models.BooleanField(default=False, verbose_name=b'Mail Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_end',
            field=models.DateField(null=True, verbose_name=b'Mail Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_excuse_required',
            field=models.BooleanField(default=False, verbose_name=b'Mail Voting Method Excuse Required?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_instructions',
            field=models.TextField(verbose_name=b'Mail Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_isprimary',
            field=models.BooleanField(default=False, verbose_name=b'Mail Voting Primary Method?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='mail_voting_start',
            field=models.DateField(null=True, verbose_name=b'Mail Voting Method Start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_enabled',
            field=models.BooleanField(default=False, verbose_name=b'Online Voting Enabled?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_end',
            field=models.DateField(null=True, verbose_name=b'Online Voting Method End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_excuse_required',
            field=models.BooleanField(default=False, verbose_name=b'Online Voting Method Excuse Required?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_instructions',
            field=models.TextField(verbose_name=b'Online Voting Method Instructions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_isprimary',
            field=models.BooleanField(default=False, verbose_name=b'Online Primary Method?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='online_voting_start',
            field=models.DateField(null=True, verbose_name=b'Online Voting Method Start', blank=True),
            preserve_default=True,
        ),
    ]

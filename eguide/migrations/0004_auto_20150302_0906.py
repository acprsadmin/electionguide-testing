# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0003_institution_quota'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='cedaw_ratified',
            field=models.CharField(help_text=b'Leave blank is the answer is NO. e.g. Yes (since 24 July 1985)', max_length=250, null=True, verbose_name=b'CIDAW ratified', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='cedaw_signatory',
            field=models.CharField(help_text=b'Leave blank is the answer is NO. e.g. Yes (since 24 July 1980)', max_length=250, null=True, verbose_name=b'CIDAW signatory', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='hdi_position',
            field=models.IntegerField(default=0, verbose_name=b'Human Development Index (HDI) Position'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='sigi',
            field=models.CharField(help_text=b'22nd out of 86 non-OECD countries (latest rankings are from 2012)', max_length=250, null=True, verbose_name=b'Social Institutions and Gender Index', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='female_elected',
            field=models.IntegerField(default=0, help_text=b'Only enter a number of female elected officials such as parliament members, presidents, members of the assembly, etc.', verbose_name=b'Number of female elected leaders'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='population_female',
            field=models.IntegerField(help_text=b'Population must be entered as numbers with no commas or separators, e.g. 39456123', null=True, verbose_name=b'Female Population', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='population_male',
            field=models.IntegerField(help_text=b'Population must be entered as numbers with no commas or separators, e.g. 39456123', null=True, verbose_name=b'Male Population', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='registered_voters_female',
            field=models.IntegerField(help_text=b'Number of registered voters with no commas or separators, e.g. 39456123', null=True, verbose_name=b'Female Registered Voters', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='registered_voters_male',
            field=models.IntegerField(help_text=b'Number of registered voters with no commas or separators, e.g. 39456123', null=True, verbose_name=b'Male Registered Voters', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name=b'Gender', choices=[(b'f', b'Female'), (b'm', b'Male')]),
            preserve_default=True,
        ),
    ]

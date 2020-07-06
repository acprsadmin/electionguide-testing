# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0009_election_voter_registration_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='election_scope',
            field=models.ForeignKey(blank=True, to='eguide.Election_scope', help_text=b'*NEW*', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='is_national_exec',
            field=models.BooleanField(default=False, verbose_name=b'NATIONAL_EXEC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='is_national_legislative',
            field=models.BooleanField(default=False, verbose_name=b'NATIONAL_LEGISLATIVE'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='is_national_lower',
            field=models.BooleanField(default=False, verbose_name=b'NATIONAL_LOWER'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='is_national_upper',
            field=models.BooleanField(default=False, verbose_name=b'NATIONAL_UPPER'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0007_auto_20200408_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='cso_comments',
            field=models.TextField(verbose_name=b'CSO Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='cso_confirmation',
            field=models.BooleanField(default=False, verbose_name=b'CSO Confirmation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='cso_confirmation_date',
            field=models.DateField(null=True, verbose_name=b'CSO Confirmation Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='cso_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'CSO Confirmation Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='embassy_comments',
            field=models.TextField(verbose_name=b'Embassy Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='embassy_confirmation',
            field=models.BooleanField(default=False, verbose_name=b'Embassy Confirmation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='embassy_confirmation_date',
            field=models.DateField(null=True, verbose_name=b'Embassy Confirmation Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='embassy_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Embassy Confirmation Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='ifes_comments',
            field=models.TextField(verbose_name=b'IFES Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='ifes_confirmation',
            field=models.BooleanField(default=False, verbose_name=b'IFES Confirmation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='ifes_confirmation_date',
            field=models.DateField(null=True, verbose_name=b'IFES Confirmation Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='ifes_confirmation_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'IFES Confirmation Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='legal_consultant_comments',
            field=models.TextField(verbose_name=b'Consultant Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='legal_consultant_confirmation',
            field=models.BooleanField(default=False, verbose_name=b'Legal Consultant Confirmation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='legal_consultant_confirmation_date',
            field=models.DateField(null=True, verbose_name=b'Legal Consultant Confirmation Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='legal_consultant_name',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Legal Consultant Name'),
            preserve_default=True,
        ),
    ]

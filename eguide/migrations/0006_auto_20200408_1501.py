# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0005_auto_20200408_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='disinformation_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Disinforamtion Details'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='disinformation_prohibition',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Disinformation Prohibited?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='disinformation_prohibition_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Disinformation Prohibition Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='electoral_rights_info_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Electoral Rights Info Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='hate_speech_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Hate Speech Details'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='hate_speech_prohibition',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Hate Speech Prohibited?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='hate_speech_prohibition_source',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Hate Speech Prohibition Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='restrict_electoral_rights',
            field=models.BooleanField(default=False, verbose_name=b'Restrict Electoral Rights?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='restrict_electoral_rights_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Restrict Electoral Rights Details'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='support_electoral_rights',
            field=models.BooleanField(default=False, verbose_name=b'Support Electoral Rights?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='support_electoral_rights_details',
            field=models.CharField(max_length=400, null=True, verbose_name=b'Support Electoral Rights Detail'),
            preserve_default=True,
        ),
    ]

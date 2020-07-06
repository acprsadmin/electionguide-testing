# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0018_auto_20200509_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='yn_disinformation_prohibited',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Is Disinformation Prohibited?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_early_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Online Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_hate_speech_prohibited',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Is Hate Speech Prohibited?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_inperson_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Online Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_mail_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Online Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_online_voting_excuse_required',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Online Voting Method Excuse Required?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_restrict_electoral_rights',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Support Electoral Rights?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='yn_support_electoral_rights',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Support Electoral Rights?', choices=[(1, b'Yes'), (2, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='disinformation_prohibition',
            field=models.TextField(null=True, verbose_name=b'Disinformation Prohibited Details', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='hate_speech_prohibition',
            field=models.TextField(null=True, verbose_name=b'Hate Speech Prohibited Detials', blank=True),
            preserve_default=True,
        ),
    ]

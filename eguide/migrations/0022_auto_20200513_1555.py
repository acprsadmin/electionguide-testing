# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0021_auto_20200512_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election_API',
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
        migrations.AlterField(
            model_name='election',
            name='election_declared_start_date',
            field=models.DateField(help_text=b'', null=True, verbose_name=b'Election Declared Start', blank=True),
            preserve_default=True,
        ),
    ]

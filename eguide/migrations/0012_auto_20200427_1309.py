# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eguide', '0011_auto_20200426_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name=b'Approved for Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='is_submitted',
            field=models.BooleanField(default=False, verbose_name=b'Submitted for Approval'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='published_by',
            field=models.IntegerField(null=True, verbose_name=b'Published by', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='election',
            name='submitted_by',
            field=models.IntegerField(null=True, verbose_name=b'Submitted by', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='election',
            name='original_election_year',
            field=models.IntegerField(blank=True, help_text=b'Original Year of the Election', null=True, verbose_name=b'Original Election Year', choices=[(1990, b'1990'), (1991, b'1991'), (1992, b'1992'), (1993, b'1993'), (1994, b'1994'), (1995, b'1995'), (1996, b'1996'), (1997, b'1997'), (1998, b'1998'), (1999, b'1999'), (2000, b'2000'), (2001, b'2001'), (2002, b'2002'), (2003, b'2003'), (2004, b'2004'), (2005, b'2005'), (2006, b'2006'), (2007, b'2007'), (2008, b'2008'), (2009, b'2009'), (2010, b'2010'), (2011, b'2011'), (2012, b'2012'), (2013, b'2013'), (2014, b'2014'), (2015, b'2015'), (2016, b'2016'), (2017, b'2017'), (2018, b'2018'), (2019, b'2019'), (2020, b'2020'), (2021, b'2021'), (2022, b'2022'), (2023, b'2023'), (2024, b'2024'), (2025, b'2025'), (2026, b'2026'), (2027, b'2027'), (2028, b'2028'), (2029, b'2029'), (2030, b'2030'), (2031, b'2031'), (2032, b'2032'), (2033, b'2033'), (2034, b'2034'), (2035, b'2035'), (2036, b'2036'), (2037, b'2037'), (2038, b'2038'), (2039, b'2039')]),
            preserve_default=True,
        ),
    ]

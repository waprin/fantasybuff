# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0016_auto_20141015_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamreportcard',
            name='draft_rank',
        ),
        migrations.RemoveField(
            model_name='teamreportcard',
            name='lineup_rank',
        ),
        migrations.RemoveField(
            model_name='teamreportcard',
            name='trade_rank',
        ),
        migrations.RemoveField(
            model_name='teamreportcard',
            name='waiver_rank',
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='average_draft_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='average_lineup_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='average_trade_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='average_waiver_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
    ]

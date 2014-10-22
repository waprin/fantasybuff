# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0017_auto_20141016_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaguereportcard',
            name='draft_maxmin',
        ),
        migrations.RemoveField(
            model_name='leaguereportcard',
            name='league',
        ),
        migrations.RemoveField(
            model_name='leaguereportcard',
            name='lineup_maxmin',
        ),
        migrations.RemoveField(
            model_name='leaguereportcard',
            name='trade_maxmin',
        ),
        migrations.RemoveField(
            model_name='leaguereportcard',
            name='waiver_maxmin',
        ),
        migrations.DeleteModel(
            name='LeagueReportCard',
        ),
        migrations.RemoveField(
            model_name='metricmaxandmin',
            name='league',
        ),
        migrations.RemoveField(
            model_name='metricmaxandmin',
            name='max_team',
        ),
        migrations.RemoveField(
            model_name='metricmaxandmin',
            name='min_team',
        ),
        migrations.DeleteModel(
            name='MetricMaxAndMin',
        ),
        migrations.AddField(
            model_name='teamweekscores',
            name='lineup_score',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teamreportcard',
            name='average_lineup_score',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=4),
        ),
    ]

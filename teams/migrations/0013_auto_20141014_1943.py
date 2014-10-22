# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_auto_20141014_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricmaxandmin',
            name='league',
            field=models.OneToOneField(null=True, to='teams.League'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metricmaxandmin',
            name='max_week',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metricmaxandmin',
            name='min_week',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='leaguereportcard',
            name='draft_maxmin',
            field=models.ForeignKey(related_name=b'draft', to='teams.MetricMaxAndMin', null=True),
        ),
        migrations.AlterField(
            model_name='leaguereportcard',
            name='league',
            field=models.OneToOneField(null=True, to='teams.League'),
        ),
        migrations.AlterField(
            model_name='leaguereportcard',
            name='lineup_maxmin',
            field=models.ForeignKey(related_name=b'lineup', to='teams.MetricMaxAndMin', null=True),
        ),
        migrations.AlterField(
            model_name='leaguereportcard',
            name='trade_maxmin',
            field=models.ForeignKey(related_name=b'trade', to='teams.MetricMaxAndMin', null=True),
        ),
        migrations.AlterField(
            model_name='leaguereportcard',
            name='waiver_maxmin',
            field=models.ForeignKey(related_name=b'waiver', to='teams.MetricMaxAndMin', null=True),
        ),
        migrations.AlterField(
            model_name='leagueweekscores',
            name='lineup_average',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='metricmaxandmin',
            name='max_team',
            field=models.ForeignKey(related_name=b'max_team', to='teams.Team', null=True),
        ),
        migrations.AlterField(
            model_name='metricmaxandmin',
            name='max_value',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='metricmaxandmin',
            name='min_team',
            field=models.ForeignKey(related_name=b'min_team', to='teams.Team', null=True),
        ),
        migrations.AlterField(
            model_name='metricmaxandmin',
            name='min_value',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=4),
        ),
    ]

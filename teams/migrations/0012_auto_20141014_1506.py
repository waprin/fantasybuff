# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_auto_20141009_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueReportCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueWeekScores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField()),
                ('lineup_average', models.DecimalField(max_digits=7, decimal_places=4)),
                ('trade_average', models.DecimalField(max_digits=7, decimal_places=4)),
                ('draft_average', models.DecimalField(max_digits=7, decimal_places=4)),
                ('waiver_average', models.DecimalField(max_digits=7, decimal_places=4)),
                ('league', models.OneToOneField(to='teams.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricMaxAndMin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_value', models.DecimalField(max_digits=7, decimal_places=4)),
                ('min_value', models.DecimalField(max_digits=7, decimal_places=4)),
                ('max_team', models.ForeignKey(related_name=b'max_team', to='teams.Team')),
                ('min_team', models.ForeignKey(related_name=b'min_team', to='teams.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leaguereportcard',
            name='draft_maxmin',
            field=models.ForeignKey(related_name=b'draft', to='teams.MetricMaxAndMin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguereportcard',
            name='league',
            field=models.OneToOneField(to='teams.League'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguereportcard',
            name='lineup_maxmin',
            field=models.ForeignKey(related_name=b'lineup', to='teams.MetricMaxAndMin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguereportcard',
            name='trade_maxmin',
            field=models.ForeignKey(related_name=b'trade', to='teams.MetricMaxAndMin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguereportcard',
            name='waiver_maxmin',
            field=models.ForeignKey(related_name=b'waiver', to='teams.MetricMaxAndMin'),
            preserve_default=True,
        ),
    ]

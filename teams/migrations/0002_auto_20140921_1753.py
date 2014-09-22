# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerScoreStats',
            fields=[
                ('score_entry', models.OneToOneField(primary_key=True, serialize=False, to='teams.ScoreEntry')),
                ('pass_yards', models.IntegerField()),
                ('pass_td', models.IntegerField()),
                ('interceptions', models.IntegerField()),
                ('run_attempts', models.IntegerField()),
                ('run_yards', models.IntegerField()),
                ('run_td', models.IntegerField()),
                ('receptions', models.IntegerField()),
                ('reception_yards', models.IntegerField()),
                ('reception_td', models.IntegerField()),
                ('blocked_kr', models.IntegerField()),
                ('int_td', models.IntegerField()),
                ('fr_td', models.IntegerField()),
                ('return_td', models.IntegerField()),
                ('default_points', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='scoreentry',
            unique_together=set([('week', 'player')]),
        ),
        migrations.RemoveField(
            model_name='scoreentry',
            name='league',
        ),
        migrations.AddField(
            model_name='scoreentry',
            name='year',
            field=models.CharField(default='2014', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adddrop',
            name='waiver',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='actual',
            field=models.BooleanField(default=False),
        ),
    ]

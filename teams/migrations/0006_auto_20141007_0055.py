# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_scorecard_delta'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamWeekScores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft_score', models.DecimalField(max_digits=7, decimal_places=4)),
                ('league', models.ForeignKey(to='teams.League', null=True)),
                ('team', models.ForeignKey(to='teams.Team', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=20, null=True, choices=[('QB', b'Quarterback'), ('WR', b'Wide Receiver'), ('RB', b'Running Back'), ('TE', b'Tight End'), ('D/ST', b'Defense/Special Teams'), ('K', b'Kicker')]),
        ),
    ]

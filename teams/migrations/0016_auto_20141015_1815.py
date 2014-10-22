# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0015_auto_20141014_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamreportcard',
            name='lineup_score',
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='draft_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='lineup_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='trade_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamreportcard',
            name='waiver_rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

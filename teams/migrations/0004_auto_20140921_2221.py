# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_remove_scoreentry_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscorestats',
            name='score_entry',
            field=models.OneToOneField(related_name=b'player_score_stats', primary_key=True, serialize=False, to='teams.ScoreEntry'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_tradeentry_other_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adddrop',
            name='player_added',
        ),
        migrations.RemoveField(
            model_name='adddrop',
            name='player_dropped',
        ),
        migrations.AddField(
            model_name='adddrop',
            name='added',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adddrop',
            name='player',
            field=models.ForeignKey(default=None, to='teams.Player'),
            preserve_default=False,
        ),
    ]

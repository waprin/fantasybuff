# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_auto_20141014_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leagueweekscores',
            name='league',
            field=models.ForeignKey(to='teams.League'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0023_league_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddrop',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='draftclaim',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tradeentry',
            name='date',
            field=models.DateTimeField(),
        ),
    ]

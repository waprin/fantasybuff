# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0018_espnuser_allow_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='abbreviation',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='espn_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

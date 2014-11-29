# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0005_espnuser_allow_save'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='espn_user',
            field=models.ForeignKey(blank=True, to='teams.EspnUser', null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='owner_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

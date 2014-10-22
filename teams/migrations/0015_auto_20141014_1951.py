# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0014_auto_20141014_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricmaxandmin',
            name='league',
            field=models.ForeignKey(to='teams.League', null=True),
        ),
    ]

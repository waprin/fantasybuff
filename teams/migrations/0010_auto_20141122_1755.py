# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0009_auto_20141122_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddrop',
            name='added',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='espn_id',
            field=models.CharField(max_length=20, unique=True, null=True),
        ),
    ]

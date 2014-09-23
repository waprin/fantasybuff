# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20140923_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='espn_id',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0016_auto_20141124_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='scraped_weeks',
            field=models.IntegerField(default=11),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0019_auto_20141126_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='scraped_weeks',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20141008_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamweekscores',
            name='trade_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamweekscores',
            name='waiver_score',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
    ]

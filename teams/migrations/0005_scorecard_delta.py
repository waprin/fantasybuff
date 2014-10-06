# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20141004_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecard',
            name='delta',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0020_auto_20141126_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='espnuser',
            name='calculating',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0021_espnuser_calculating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='espnuser',
            name='calculating',
        ),
        migrations.AddField(
            model_name='league',
            name='calculating',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_espnuser_loaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='espnuser',
            name='failed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

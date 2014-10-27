# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0020_league_failed'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='loading',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

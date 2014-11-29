# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0011_player_other_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecardentry',
            name='week',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

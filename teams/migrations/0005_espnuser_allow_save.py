# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0004_auto_20141118_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='espnuser',
            name='allow_save',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
